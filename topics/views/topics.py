from urllib.parse import urlparse
import bleach
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.db import transaction
from django.template import loader, RequestContext
from django.template.defaultfilters import register
from django.utils import safestring
import markdown
import re
import json
import reversion as revisions
from topics.helpers.user_permissions import user_can_edit
from topics.models import Topic, BadTopicPath, TopicSite

www_remover = lambda _, r=re.compile("^www\."): r.sub("", _)


def url_handler(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    output_url = parsed.geturl()
    domain = www_remover(parsed.netloc)
    domain_link = "{}://{}".format(parsed.scheme, domain)
    return domain, domain_link, output_url


def process(input_string):
    if any(input_string.strip()):
        data = json.loads(input_string)
        for item in data:
            for data_type, d in item.items():
                if data_type == "link":
                    d['url'] = url_handler(d['url'])
        return data
    else:
        return []


@register.filter(name='markdownify')
def markdownify(value):
    return safestring.mark_safe(markdown.markdown(value))


@register.filter(name='un_markdownify')
def un_markdownify(value):
    return safestring.mark_safe(value)


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def get_topic(request, topic_name, retry=False):
    if not request.path.endswith("/"):
        return redirect(request.path + "/")

    topic_name = topic_name[:50]
    topic_path = tuple(topic_name.strip("/").split("/"))
    topic_path_is_root = (topic_path == ("",))

    if topic_path[-1] == "_new":
        short_topic_path = () if len(topic_path) == 1 else topic_path[:-1]
        return new_topic(request, short_topic_path)

    is_editing = False
    if topic_path[-1] == "_edit":
        is_editing = True
        topic_path = topic_path[:-1]
        if len(topic_path) == 0:
            topic_path_is_root = True
            topic_path = ("",)

    if not topic_path_is_root:
        topics = list(Topic.get_topics(get_current_site(request), topic_path))
        topic_id = None
        for topic in topics[-2]:
            if topic['name'].lower() == topic_path[-1].lower():
                topic_id = topic['id']
    else:
        topics = [Topic.get_tree_top(get_current_site(request))]
        try:
            topic_id = Topic.get_from_path(get_current_site(request), topic_path, None)['id']
        except BadTopicPath:
            if not retry:
                Topic(orig_name="", parent_id=None, site=get_current_site(request)).save()
                return get_topic(request, '', retry=True)
            else:
                raise

    try:
        topic = Topic.get_from_id(topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")

    if is_editing and request.POST:
        return edit_topic(request, topic)
    elif is_editing:
        template = loader.get_template('topics/edit_topic.html')
    else:
        template = loader.get_template('topics/show_topic.html')

    resources = process(topic.text)

    extra_empty_topic = {'path': topic_path + ("",)}

    context = RequestContext(request, {
        'topics': topics,
        'nav_active': topic_path,
        'is_editing': is_editing,
        'extra_empty_topic': extra_empty_topic,
        'topic_path_is_root': topic_path_is_root,
        'resources': resources
    })
    if is_editing and not TopicSite.get_from_request(request).can_user_edit(request.user.id):
        raise PermissionDenied

    return HttpResponse(template.render(context))


@user_can_edit
@transaction.atomic()
@revisions.create_revision()
def new_topic(request, topic_path):
    error = ""
    if request.POST:
        topic_name = request.POST.get('name')
        if len(topic_path) == 0:
            parent = None
        else:
            parent = Topic.get_from_path(get_current_site(request), topic_path)['id']
        if topic_name:
            topic_to_save = Topic(orig_name=topic_name, parent_id=parent, site=get_current_site(request))
            try:
                if parent is None and topic_name[-4:] in {'.txt', '.xml'}:
                    error_message = "Top level topics can't end in .txt or .xml for technical reasons. Sorry."
                    raise ValidationError({'name': error_message})
                topic_to_save.full_clean()
            except ValidationError as e:
                for field, error_list in e.message_dict.items():
                    error += "".join(error_list) + " "
            else:
                topic_to_save.save()
                revisions.set_user(request.user)
                return redirect(reverse('topics:get_topic', args=[topic_to_save.name]))

    template = loader.get_template('topics/new_topic.html')
    extra_empty_topic = {'path': topic_path + ("",)}
    if any(topic_path):
        topics = list(Topic.get_topics(get_current_site(request), topic_path))
        context = RequestContext(request, {
            'topics': topics,
            'nav_active': topic_path,
            'new_topic': 'new-topic',
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    else:
        context = RequestContext(request, {
            'topics': [Topic.get_tree_top(get_current_site(request))],
            'new_topic': 'new-topic',
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    return HttpResponse(template.render(context))


@user_can_edit
@transaction.atomic()
@revisions.create_revision()
def edit_topic(request, topic):
    if request.POST:
        topic.text = json.dumps(json.loads(bleach.clean(request.POST.get('text'))))
        topic.save()
        revisions.set_user(request.user)
        return redirect('..')

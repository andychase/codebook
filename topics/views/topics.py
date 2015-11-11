from urllib.parse import urlparse
import bleach
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.db import transaction, IntegrityError
from django.template import loader, RequestContext
from django.template.defaultfilters import register
from django.utils import safestring
import markdown
import re
import json
import reversion as revisions
from reddit_cssfilter import cssfilter
from topics.helpers.user_permissions import user_can_edit
from topics.models import Topic, BadTopicPath, TopicSite, TopicSiteData
from topics.views.home_about import site_not_found

duplicate_topic_warning = """
<i class="ss-alert"></i>
There was an error while renaming or rearranging topics:
a topic with that name already exists in this category.
"""


def www_remover(input_text, r=re.compile("^www\.")):
    return r.sub("", input_text)


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


def add_active_to_topic_path(topics, nav_active):
    for i, active, topic_list in zip(range(1, len(topics) + 1), nav_active, topics):
        for topic in topic_list:
            if topic['name'] == active:
                topic['active'] = True
            if i == len(nav_active):
                topic['last_nav'] = True


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
    if TopicSite.get_from_request(request) is None:
        return site_not_found(request, topic_name)
    if not request.path.endswith("/"):
        return redirect(request.path + "/")

    topic_name = topic_name[:2000]
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
                return create_top_level(request)
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
    add_active_to_topic_path(topics, topic_path)
    context = RequestContext(request, {
        'topics': topics,
        'is_editing': is_editing,
        'extra_empty_topic': extra_empty_topic,
        'topic_path_is_root': topic_path_is_root,
        'resources': resources
    })
    if is_editing and not TopicSite.get_from_request(request).can_user_edit(request.user.id):
        raise PermissionDenied

    return HttpResponse(template.render(context))


@transaction.atomic()
@revisions.create_revision()
def create_top_level(request):
    Topic(orig_name="", parent_id=None, site=get_current_site(request)).save()
    return get_topic(request, '', retry=True)


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
            deleted_topic = Topic.get_deleted(orig_name=topic_name, parent_id=parent, site=get_current_site(request))
            if any(deleted_topic):
                topic_to_save = deleted_topic.first()
                topic_to_save.active = True
                messages.warning(request, "A previously deleted topic was restored.")
            else:
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
                if not request.user.is_anonymous():
                    revisions.set_user(request.user)
                return redirect(reverse('topics:get_topic', args=[topic_to_save.full_path()]))

    template = loader.get_template('topics/new_topic.html')
    extra_empty_topic = {'path': topic_path + ("",)}
    if any(topic_path):
        topics = list(Topic.get_topics(get_current_site(request), topic_path))
        add_active_to_topic_path(topics, topic_path)
        context = RequestContext(request, {
            'topics': topics,
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


def handle_topics_sort(topic_being_edited, raw_topic_lists):
    topic_lists = []
    # Setup
    for topic_list in raw_topic_lists:
        topic_id_list = [int(item.replace("topic-", "")) for item in topic_list]
        topic_object_list = [Topic.get_from_id(item_id) for item_id in topic_id_list]
        topic_lists.append(topic_object_list)
    # Set parents of all topics
    for parent_id, topic_list in zip((None,) + topic_being_edited.full_path_ids(), topic_lists):
        for topic in topic_list:
            topic.parent_id = parent_id
    # Set order of all topics & save
    for topic_list in topic_lists:
        for index, topic in enumerate(topic_list):
            topic.order = index
            topic.save()


def edit_root_topic(request):
    css_style = request.POST.get('css_style')
    if css_style:
        stylesheet, errors = cssfilter.validate_css(css_style, [])
        if errors:
            for error in errors:
                messages.warning(request, error.message_key % error.message_params)
        else:
            TopicSiteData.update_css_style(get_current_site(request).id, stylesheet)


@user_can_edit
@revisions.create_revision()
def edit_topic(request, topic):
    if request.POST:
        if topic.name == "" and TopicSite.get_from_request(request).is_user_admin(request.user):
            edit_root_topic(request)
        schema = json.loads(bleach.clean(request.POST.get('text')))
        topics_sort = list(json.loads(request.POST.get('topics_sort', '[]')))
        rename_topic_name = request.POST.get('rename_topic_name', '').strip()
        rename_change = any(rename_topic_name) and rename_topic_name != topic.orig_name
        delete_topic = \
            len(schema) == 0 and topic.name != "" and not any(topics_sort) \
            and not rename_change and not topic.any_children()

        original_name = topic.orig_name
        try:
            with transaction.atomic():
                if rename_change:
                    topic.orig_name = rename_topic_name
                    topic.full_clean()
                    topic.save()

                if any(topics_sort):
                    handle_topics_sort(topic, topics_sort)
                    topic = Topic.get_from_id(topic.id)
        except (IntegrityError, ValidationError):
            topic.orig_name = original_name
            topic.full_clean()
            messages.warning(request, duplicate_topic_warning)

        if delete_topic:
            if topic.parent is not None:
                url_to_redirect = reverse('topics:get_topic', args=[topic.parent.full_path()])
            else:
                url_to_redirect = "/"
            topic.active = False
            topic.save()
            if not request.user.is_anonymous():
                revisions.set_user(request.user)
            return redirect(url_to_redirect)
        else:
            topic.text = json.dumps(schema)
            topic.save()
            if not request.user.is_anonymous():
                revisions.set_user(request.user)
            return redirect(reverse('topics:get_topic', args=[topic.full_path()]))

import bleach
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from django.template import loader, RequestContext
from django.template.defaultfilters import register
from django.utils import safestring
import markdown

from topics.models import Topic
from topics.parser import process


@register.filter(name='markdownify')
def markdownify(value):
    return safestring.mark_safe(markdown.markdown(value))


@register.filter(name='un_markdownify')
def un_markdownify(value):
    return safestring.mark_safe(value.replace("\n", "<br>"))


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def add_link_helpers(resources):
    last_block_is_section = False
    last_block_is_subsection = False
    output = []
    for resource in resources:
        if resource.section:
            last_block_is_section = True
        elif resource.subsection:
            last_block_is_subsection = True
        elif resource.link:
            if not last_block_is_section:
                if last_block_is_subsection:
                    output.insert(-1, resource._replace(link=None, section=""))
                else:
                    output.append(resource._replace(link=None, section=""))
                    output.append(resource._replace(link=None, subsection=""))
            elif not last_block_is_subsection:
                output.append(resource._replace(link=None, subsection=""))
            last_block_is_section = False
            last_block_is_subsection = False
        output.append(resource)
    return output


def get_topic(request, topic_name):
    if not request.path.endswith("/"):
        return redirect(request.path + "/")

    topic_name = topic_name[:50]
    topic_path = tuple(topic_name.strip("/").split("/"))

    if topic_path[-1] == "new_topic":
        short_topic_path = () if len(topic_path) == 1 else topic_path[:-1]
        return new_topic(request, short_topic_path)

    is_editing = False
    if topic_path[-1] == "edit":
        is_editing = True
        topic_path = topic_path[:-1]

    topics = list(Topic.get_topics(topic_path))
    topic_id = None
    for topic in topics[-2]:
        if topic['name'].lower() == topic_path[-1].lower():
            topic_id = topic['id']
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")

    if is_editing and request.POST:
        return edit_topic(request, topic)
    elif is_editing:
        template = loader.get_template('topics/edit_topic.html')
        resources = add_link_helpers(process(topic.text))
    else:
        template = loader.get_template('topics/show_topic.html')
        resources = process(topic.text)

    extra_empty_topic = {'path': topic_path + ("",)}

    context = RequestContext(request, {
        'topics': topics,
        'nav_active': topic_path,
        'is_editing': is_editing,
        'extra_empty_topic': extra_empty_topic,
        'resources': resources
    })

    return HttpResponse(template.render(context))


@permission_required('topics.topic.can_create_topic')
def new_topic(request, topic_path):
    error = ""
    if request.POST:
        topic_name = request.POST.get('name')
        if len(topic_path) == 0:
            parent = None
        else:
            parent = Topic.get_from_path(topic_path)['id']
        if topic_name:
            new_topic = Topic(orig_name=topic_name, parent_id=parent)
            try:
                new_topic.full_clean()
            except ValidationError as e:
                for field, error_list in e.message_dict.items():
                    error += "".join(error_list) + " "
            else:
                new_topic.save()
                return redirect('/topics/{}/'.format("/".join(topic_path + (topic_name,)).lower()))

    template = loader.get_template('topics/new_topic.html')
    extra_empty_topic = {'path': topic_path + ("",)}
    if any(topic_path):
        topics = list(Topic.get_topics(topic_path))
        context = RequestContext(request, {
            'topics': topics,
            'nav_active': topic_path,
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    else:
        context = RequestContext(request, {
            'topics': [Topic.get_tree_top()],
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    return HttpResponse(template.render(context))


@permission_required('topics.topic.can_edit_topic')
def edit_topic(request, topic):
    if request.POST:
        topic.text = bleach.clean(request.POST.get('text'))
        topic.save()
        return redirect('..')

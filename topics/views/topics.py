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
def cut(value):
    return safestring.mark_safe(markdown.markdown(value))


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


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

    if is_editing:
        return edit_topic(request, topic_path, topic)

    extra_empty_topic = {'path': topic_path + ("",)}
    topic_data = process(topic.text)
    context = RequestContext(request, {
        'topics': topics,
        'nav_active': topic_path,
        'extra_empty_topic': extra_empty_topic,
        'resources': topic_data
    })
    template = loader.get_template('topics/show_topic.html')

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
def edit_topic(request, topic_path, topic):
    if request.POST:
        topic_text = request.POST.get('text')
        topic.text = topic_text
        topic.save()
        return redirect('..')
    else:
        template = loader.get_template('topics/edit_topic.html')

        topics = list(Topic.get_topics(topic_path))
        extra_empty_topic = {'path': topic_path + ("",)}
        context = RequestContext(request, {
            'topics': topics,
            'nav_active': topic_path,
            'extra_empty_topic': extra_empty_topic,
            'topic_text': topic.text,
            'editing_topic': True,
        })
        return HttpResponse(template.render(context))

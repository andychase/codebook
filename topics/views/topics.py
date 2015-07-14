from django.http import HttpResponse, Http404
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


def topic_data_to_stream(topic_data):
    current_section = ""
    current_subsection = ""
    if not topic_data:
        return []
    for (_, link_block, _) in topic_data:
        if link_block:
            if link_block['section'] != current_section:
                current_section = link_block['section']
                current_subsection = ""
                yield {'section': current_section}
            if link_block['subsection'] != current_subsection:
                current_subsection = link_block['subsection']
                yield {'subsection': current_subsection}
            link_block['authors'] = [safestring.mark_safe(a) for a in link_block['authors']]
            yield {'link': link_block}


def get_topic(request, topic_name):
    topic_name = topic_name[:50]
    topic_path = tuple(topic_name.strip("/").split("/"))
    topics = list(Topic.get_topics(topic_path))
    topic_id = None
    for topic in topics[-2]:
        if topic['name'].lower() == topic_path[-1].lower():
            topic_id = topic['id']

    template = loader.get_template('layouts/topic.html')
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    topic_data = topic_data_to_stream(process(topic.text))
    context = RequestContext(request, {
        'topics': topics,
        'nav_active': topic_path,
        'resources': topic_data
    })
    return HttpResponse(template.render(context))


from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.template.defaultfilters import register
from django.utils import safestring
import markdown
import yaml
from topics.models import Topic
from topics.parser import process
from topics import view_helpers

with open('./topics/config.yml') as f:
    site = yaml.safe_load(f)


@register.filter(name='markdownify')
def cut(value):
    return safestring.mark_safe(markdown.markdown(value))


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def get_tree():
    results = Topic.objects.values('name', 'parent')
    results = results.filter(parent=None)
    for t in results:
        t['level'] = 1
        t['name_lower'] = t['name'].lower()
    return results


def about(request, info_page_title):
    if info_page_title not in ['privacy', 'terms']:
        info_page_title = "about"
    with open('./topics/info/{}.md'.format(info_page_title)) as f:
        page_content = markdown.markdown(f.read())

    template = loader.get_template('layouts/page.html')
    context = RequestContext(request, {
        'site': site,
        'content': safestring.mark_safe(page_content),
        'topics': get_tree(),
        'title': info_page_title
    })
    return HttpResponse(template.render(context))


def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'site': site,
        'topics': get_tree()
    })
    return HttpResponse(template.render(context))


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
            yield {'link': link_block}


def get_topic(request, topic_name):
    topic_name = topic_name[:50]
    template = loader.get_template('layouts/topic.html')
    try:
        topic = Topic.objects.get(name__iexact=topic_name)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    topic_data = topic_data_to_stream(process(topic.text))
    context = RequestContext(request, {
        'site': site,
        'topics': get_tree(),
        'nav_active': [topic_name],
        'resources': topic_data
    })
    return HttpResponse(template.render(context))

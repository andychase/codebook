from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils import safestring
from django.contrib.sites.shortcuts import get_current_site
import markdown
from topics.models import Topic


def about(request, info_page_title):
    if info_page_title not in ['privacy', 'terms']:
        info_page_title = "about"
    with open('./topics/info/{}.md'.format(info_page_title)) as f:
        page_content = markdown.markdown(f.read())

    template = loader.get_template('layouts/page.html')
    context = RequestContext(request, {
        'content': safestring.mark_safe(page_content),
        'topics': [Topic.get_tree_top(get_current_site(request))],
        'title': info_page_title
    })
    return HttpResponse(template.render(context))


def site_not_found(request, path):
    template = loader.get_template('topics/site_not_found.html')
    context = RequestContext(request, {
        'path': path
    })
    return HttpResponse(template.render(context))

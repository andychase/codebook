import codecs

from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.utils import safestring
from django.contrib.sites.shortcuts import get_current_site
import markdown

pages = {}
for term in {'privacy', 'terms'}:
    with codecs.open('./topics/info/{}.md'.format(term), encoding='utf-8') as f:
        pages[term] = markdown.markdown(f.read())


def about(request, info_page_title):
    if info_page_title not in ['privacy', 'terms']:
        raise Http404("About page not found")

    template = loader.get_template('layouts/page.html')
    context = RequestContext(request, {
        'content': safestring.mark_safe(pages[info_page_title]),
        'title': info_page_title
    })
    return HttpResponse(template.render(context))


def site_not_found(request, path):
    template = loader.get_template('topics/site_not_found.html')
    context = RequestContext(request, {
        'path': path
    })
    return HttpResponse(template.render(context))

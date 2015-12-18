from io import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template import loader, RequestContext
from topics.helpers import view_helpers
from topics.models import Link
import lxml.html
import requests

view_helpers.setup()


def get_topic(request, topic_name):
    if request.POST:
        save_link(request, topic_name)

    template = loader.get_template('topics/show_topic.html')
    context = RequestContext(request, {
        'links': Link.get_all_links(get_current_site(request)),
    })
    return HttpResponse(template.render(context))


@login_required
def save_link(request, topic_name):
    page = requests.get(request.POST.get('url'))
    t = lxml.html.parse(StringIO(page.text))
    l = Link(
            link=request.POST.get('url'),
            title=t.find(".//title").text,
            user=request.user,
            site=get_current_site(request)
    )
    l.save()

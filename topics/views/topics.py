import urllib
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, RequestContext
from flask import url_for

from topics.helpers import view_helpers
from topics.helpers.view_helpers import normalize_url
from topics.models import Link
import lxml.html
import requests

view_helpers.setup()


def get_topic(request, topic_name):
    if request.POST:
        return save_link(request, topic_name)

    template = loader.get_template('topics/show_topic.html')
    links = Link.get_all_links(get_current_site(request))
    context = RequestContext(request, {
        'links': links,
    })
    return HttpResponse(template.render(context))


@login_required
def save_link(request, topic_name):
    # Fix url
    url_raw = request.POST.get('url')
    if not url_raw.startswith('http'):
        url_raw = 'http://' + url_raw
    url = urllib.parse.urlparse(url_raw)
    url_full = normalize_url(url)

    # Parse title & icon
    page = requests.get(url_full)
    parsed = lxml.html.parse(StringIO(page.text))
    title = parsed.find(".//title").text
    icon = None
    icon_node = parsed.xpath('.//link[contains(@rel, "icon")]')
    if icon_node:
        icon = icon_node[0].attrib.get("href")
        icon = normalize_url(urllib.parse.urlparse(icon), url.netloc)
    if not icon:
        icon = "{}://{}/favicon.ico".format(url.scheme, url.netloc)

    link = Link(
            link=url_full,
            title=title,
            icon=icon,
            user=request.user,
            site=get_current_site(request)
    )
    link.save()
    return redirect("topics:get_topic", topic_name)

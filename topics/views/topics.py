from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, RequestContext

from topics.helpers import view_helpers
from topics.models import Link, Tag

view_helpers.setup()


def get_topic(request, topic_name):
    if request.POST:
        if request.POST.get("link_tag"):
            return save_tag(request, topic_name)
        else:
            return save_link(request, topic_name)

    template = loader.get_template('topics/show_topic.html')
    selected_tags = topic_name.strip("/")
    if selected_tags:
        selected_tags = selected_tags.split("/")
    else:
        selected_tags = []
    links = Link.get_all_links(get_current_site(request), selected_tags)
    top_tags = list(Tag.get_top_tag_list(get_current_site(request), selected_tags))
    if len(links) == 1:
        top_tags = top_tags[:-1]
    context = RequestContext(request, {
        'links': links,
        'top_tags_first': top_tags[:1],
        'top_tags_rest': top_tags[1:]
    })
    return HttpResponse(template.render(context))


@login_required
def save_tag(request, topic_name):
    tag_list_raw = request.POST.get("tag_text")
    tag_list = tag_list_raw.lstrip("#").replace("#", ",").split(",")
    link_id = int(request.POST.get("link_tag"))
    Tag.save_tags(link_id, tag_list, request.user)
    return redirect("topics:get_topic", topic_name)


@login_required
def save_link(request, topic_name):
    try:
        Link.save_link(request.POST.get('url'), request.user, get_current_site(request))
    except IntegrityError:
        messages.error(request, 'Link already posted.')
    return redirect("topics:get_topic", topic_name)

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
    links = Link.get_all_links(get_current_site(request))
    context = RequestContext(request, {
        'links': links,
    })
    return HttpResponse(template.render(context))


@login_required
def save_tag(request, topic_name):
    Tag.save_tag(int(request.POST.get("link_tag")), request.POST.get("tag_text"), request.user)
    return redirect("topics:get_topic", topic_name)


@login_required
def save_link(request, topic_name):
    try:
        Link.save_link(request.POST.get('url'), request.user, get_current_site(request))
    except IntegrityError:
        messages.error(request, 'Link already posted.')
    return redirect("topics:get_topic", topic_name)

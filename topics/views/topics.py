from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template import loader, RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from topics.helpers import view_helpers
from topics.helpers.rubric import rubric
from topics.models import Link, Tag

view_helpers.setup()


def paginate_links(links, page):
    paginator = Paginator(links, 25)

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def tag_topic(request):
    if request.POST:
        if request.POST.get("link_tag"):
            save_tag(request, "")
            return redirect("topics:tag_topic")
    template = loader.get_template('topics/tag_link.html')
    context = RequestContext(request, {
        'link': Link.get_no_tag_link(current_site=get_current_site(request)),
        'rubric': rubric
    })
    return HttpResponse(template.render(context))


def get_topic(request, topic_name):
    selected_tags = topic_name.strip("/")
    if selected_tags:
        selected_tags = selected_tags.split("/")
    else:
        selected_tags = []

    if request.POST:
        if request.POST.get("link_tag"):
            return save_tag(request, topic_name)
        if request.POST.get("delete_tag"):
            return delete_tag(request, selected_tags)
        else:
            return save_link(request, topic_name)

    template = 'topics/show_topic.html'
    links = Link.get_all_links(get_current_site(request), selected_tags)
    links = paginate_links(links, request.GET.get('page'))

    top_tags = list(Tag.get_top_tag_list(get_current_site(request), selected_tags))
    if len(links) < 6:
        top_tags = top_tags[:-1]
    context = {
        'links': links,
        'top_tags_first': top_tags[:1],
        'top_tags_rest': top_tags[1:],
        'selected_tags': selected_tags
    }
    return render(request, template, context)


def get_link_icon(request, link_id):
    l = Link.objects.filter(id=int(link_id)).values('icon_data', 'icon_content_type').first()
    if not l:
        raise Http404()
    response = HttpResponse(content_type=l['icon_content_type'])
    response.write(l['icon_data'])
    return response


@login_required
def save_tag(request, topic_name):
    tag_list_raw = request.POST.get("tag_text")
    link_title = request.POST.get("link_title")
    link_delete = request.POST.get("link_delete") == "delete"
    link_id = int(request.POST.get("link_tag"))
    link_type = request.POST.get("type")
    link_difficulty = request.POST.get("difficulty")
    link_quality = request.POST.get("quality")

    tag_list = tag_list_raw.lstrip("#").replace("#", ",").split(",")
    Link.save_ratings(link_id, link_type, link_difficulty, link_quality)
    if link_delete:
        Link.delete_link(link_id)
    else:
        if link_title:
            Link.rename_link(link_id, link_title)
        Tag.save_tags(link_id, tag_list, request.user)
    return redirect("topics:get_topic", topic_name)


@login_required
def delete_tag(_, selected_tags):
    Tag.delete_tag(selected_tags[-1])
    return redirect("topics:get_topic", selected_tags[:-1])


@login_required
def save_link(request, topic_name):
    try:
        Link.save_link(request.POST.get('url'), request.user, get_current_site(request))
    except IntegrityError:
        messages.error(request, 'Link already posted.')
    return redirect("topics:get_topic", topic_name)

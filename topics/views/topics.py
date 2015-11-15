import reversion as revisions
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader, RequestContext

from topics.helpers import view_helpers
from topics.models import Topic, BadTopicPath, TopicSite
from topics.views.home_about import site_not_found
from topics.views.topics_edit import edit_topic
from topics.views.topics_new import create_top_level, new_topic

view_helpers.setup()


def get_topic(request, topic_name, retry=False):
    if TopicSite.get_from_request(request) is None:
        return site_not_found(request, topic_name)
    if not request.path.endswith("/"):
        return redirect(request.path + "/")

    topic_name = topic_name[:2000]
    topic_path = tuple(topic_name.strip("/").split("/"))
    topic_path_is_root = (topic_path == ("",))

    if topic_path[-1] == "_new":
        short_topic_path = () if len(topic_path) == 1 else topic_path[:-1]
        return new_topic(request, short_topic_path)

    is_editing = False
    is_history = False
    if topic_path[-1] == "_edit":
        is_editing = True
        topic_path = topic_path[:-1]
        if len(topic_path) == 0:
            topic_path_is_root = True
            topic_path = ("",)

    if topic_path[-1] == "_history":
        is_history = True
        topic_path = topic_path[:-1]
        if len(topic_path) == 0:
            topic_path_is_root = True
            topic_path = ("",)

    if not topic_path_is_root:
        topics = list(Topic.get_topics(get_current_site(request), topic_path))
        topic_id = None
        for topic in topics[-2]:
            if topic['name'].lower() == topic_path[-1].lower():
                topic_id = topic['id']
    else:
        topics = [Topic.get_tree_top(get_current_site(request))]
        try:
            topic_id = Topic.get_from_path(get_current_site(request), topic_path, None)['id']
        except BadTopicPath:
            if not retry:
                create_top_level(request)
                return get_topic(request, '', retry=True)
            else:
                raise

    try:
        topic = Topic.get_from_id(topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")

    if is_editing and request.POST:
        return edit_topic(request, topic)
    elif is_editing:
        template = loader.get_template('topics/edit_topic.html')
    elif is_history:
        is_history = revisions.get_for_object(topic)
        template = loader.get_template('topics/history_topic.html')
    else:
        template = loader.get_template('topics/show_topic.html')

    resources = view_helpers.process(topic.text)

    extra_empty_topic = {'path': topic_path + ("",)}
    view_helpers.add_active_to_topic_path(topics, topic_path)
    context = RequestContext(request, {
        'topics': topics,
        'is_editing': is_editing,
        'is_history': is_history,
        'extra_empty_topic': extra_empty_topic,
        'topic_path_is_root': topic_path_is_root,
        'resources': resources
    })
    if is_editing and not TopicSite.get_from_request(request).can_user_edit(request.user.id):
        raise PermissionDenied

    return HttpResponse(template.render(context))

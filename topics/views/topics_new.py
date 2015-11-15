import reversion as revisions
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, RequestContext
from topics.helpers import view_helpers
from topics.helpers.user_permissions import user_can_edit
from topics.helpers.view_helpers import add_active_to_topic_path
from topics.models import Topic


def create_new_topic(request, topic_path):
    topic_name = request.POST.get('name')
    error = ""
    if len(topic_path) == 0:
        parent = None
    else:
        parent = Topic.get_from_path(get_current_site(request), topic_path)['id']
    if topic_name:
        deleted_topic = Topic.get_deleted(orig_name=topic_name, parent_id=parent, site=get_current_site(request))
        if any(deleted_topic):
            topic_to_save = deleted_topic.first()
            topic_to_save.active = True
            messages.warning(request, "A previously deleted topic was restored.")
        else:
            topic_to_save = Topic(orig_name=topic_name, parent_id=parent, site=get_current_site(request))
        try:
            if parent is None and topic_name[-4:] in {'.txt', '.xml'}:
                error_message = "Top level topics can't end in .txt or .xml for technical reasons. Sorry."
                raise ValidationError({'name': error_message})
            topic_to_save.full_clean()
        except ValidationError as e:
            for field, error_list in e.message_dict.items():
                error += "".join(error_list) + " "
        else:
            topic_to_save.save()
            if not request.user.is_anonymous():
                revisions.set_user(request.user)
            return error, redirect(reverse('topics:get_topic', args=[topic_to_save.full_path()]))
    return error, None


@user_can_edit
@transaction.atomic()
@revisions.create_revision()
def new_topic(request, topic_name):
    topic_path, topic_path_is_root = view_helpers.topic_name_to_path(topic_name)
    if topic_path_is_root:
        topic_path = tuple()

    error = ""
    if request.POST:
        error, result = create_new_topic(request, topic_path)
        if result is not None:
            return result

    template = loader.get_template('topics/new_topic.html')
    extra_empty_topic = {'path': topic_path + ("",)}
    if any(topic_path):
        topics = list(Topic.get_topics(get_current_site(request), topic_path))
        add_active_to_topic_path(topics, topic_path)
        context = RequestContext(request, {
            'topics': topics,
            'new_topic': 'new-topic',
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    else:
        context = RequestContext(request, {
            'topics': [Topic.get_tree_top(get_current_site(request))],
            'new_topic': 'new-topic',
            'extra_empty_topic': extra_empty_topic,
            'error': error,
            'editing_topic': True,
        })
    return HttpResponse(template.render(context))

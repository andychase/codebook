import json

import bleach
import reversion as revisions
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.shortcuts import redirect
from topics.helpers import caching

from topics.helpers import view_helpers
from topics.helpers.user_permissions import user_can_edit
from topics.models import Topic


def handle_topics_sort(topic_being_edited, raw_topic_lists):
    topic_lists = []
    # Setup
    for topic_list in raw_topic_lists:
        topic_id_list = [int(item.replace("topic-", "")) for item in topic_list]
        topic_object_list = [Topic.get_from_id(item_id) for item_id in topic_id_list]
        topic_lists.append(topic_object_list)
    # Set parents of all topics
    for parent_id, topic_list in zip((None,) + topic_being_edited.full_path_ids(), topic_lists):
        for topic in topic_list:
            topic.parent_id = parent_id
    # Set order of all topics & save
    for topic_list in topic_lists:
        for index, topic in enumerate(topic_list):
            topic.order = index
            topic.save()


@user_can_edit
@revisions.create_revision()
def edit_topic(request, topic, topic_name):
    if request.POST:
        schema = json.loads(bleach.clean(request.POST.get('text')))
        topics_sort = list(json.loads(request.POST.get('topics_sort', '[]')))
        rename_topic_name = request.POST.get('rename_topic_name', '').strip()
        rename_change = any(rename_topic_name) and rename_topic_name != topic.orig_name
        delete_topic = \
            len(schema) == 0 and topic.name != "" and not any(topics_sort) \
            and not rename_change and not topic.any_children()

        original_name = topic.orig_name
        try:
            with transaction.atomic():
                if rename_change:
                    topic.orig_name = rename_topic_name
                    topic.full_clean()
                    topic.save()
                    caching.clear_site(get_current_site(request).domain)

                if any(topics_sort):
                    handle_topics_sort(topic, topics_sort)
                    topic = Topic.get_from_id(topic.id)
                    caching.clear_site(get_current_site(request).domain)
        except (IntegrityError, ValidationError):
            topic.orig_name = original_name
            topic.full_clean()
            messages.warning(request, view_helpers.duplicate_topic_warning)

        if delete_topic:
            if topic.parent is not None:
                url_to_redirect = reverse('topics:get_topic', args=[topic.parent.full_path()])
            else:
                url_to_redirect = "/"
            topic.active = False
            caching.clear_site(get_current_site(request).domain)
            topic.save()
            if not request.user.is_anonymous():
                revisions.set_user(request.user)
            return redirect(url_to_redirect)
        else:
            topic.text = json.dumps(schema)
            caching.clear_topic(get_current_site(request).domain, topic_name)
            topic.save()
            if not request.user.is_anonymous():
                revisions.set_user(request.user)
            return redirect(reverse('topics:get_topic', args=[topic.full_path()]))

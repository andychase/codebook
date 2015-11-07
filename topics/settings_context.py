from topics.models import TopicSite


def settings_context(request):
    site = TopicSite.get_from_request(request)
    return {
        'site': site,
        'user_can_edit': site.can_user_edit(request.user.id)
    }

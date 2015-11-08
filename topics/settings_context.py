from topics.models import TopicSite


def settings_context(request):
    site = TopicSite.get_from_request(request)
    if site:
        user_can_edit = site.can_user_edit(request.user.id)
    else:
        site = {}
        user_can_edit = False
    return {
        'site': site,
        'user_can_edit': user_can_edit
    }

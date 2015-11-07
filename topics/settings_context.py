from django.contrib.sites.shortcuts import get_current_site

from topics.models import TopicSite


def settings_context(request):
    return {
        'site': TopicSite.objects.filter(site_ptr_id=get_current_site(request)).first()
    }

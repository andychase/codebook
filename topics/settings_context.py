from django.contrib.sites.shortcuts import get_current_site
from topics.models import TopicSite, TopicSiteData

logos = {
    'snc': 'snc.svg'
}


def settings_context(request):
    site = TopicSite.get_from_request(request)
    if site:
        user_can_edit = site.can_user_edit(request.user.id)
        user_is_admin = site.is_user_admin(request.user)
        site.css = TopicSiteData.get_css_style(get_current_site(request).id)
        site_logo = logos.get(site.name, 'logo.svg')
    else:
        site = {}
        site_logo = 'logo.svg'
        user_can_edit = False
        user_is_admin = False
    return {
        'site': site,
        'site_logo': 'logos/' + site_logo,
        'user_can_edit': user_can_edit,
        'user_is_admin': user_is_admin,
        'html_body_only': request.GET.get('html_body_only', False) == 'true'
    }

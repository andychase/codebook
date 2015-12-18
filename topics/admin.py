from django.contrib import admin
from .models import TopicSite, TopicSiteData, Link
import reversion


class TopicAdmin(reversion.VersionAdmin):
    list_display = ('full_path', 'site', 'pub_date')


admin.site.register(Link)
admin.site.register(TopicSite)
admin.site.register(TopicSiteData)

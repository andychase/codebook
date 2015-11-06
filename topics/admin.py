from django.contrib import admin
from .models import Topic, Site, TopicSite
import reversion


class TopicAdmin(reversion.VersionAdmin):
    list_display = ('full_path', 'site', 'pub_date')


admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicSite)

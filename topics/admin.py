from django.contrib import admin
from .models import TopicSite, TopicSiteData, Link, Tag


class TopicAdmin(admin.ModelAdmin):
    list_display = ('full_path', 'site', 'pub_date')


admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(TopicSite)
admin.site.register(TopicSiteData)

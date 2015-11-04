from django.contrib import admin
from .models import Topic
import reversion


class TopicAdmin(reversion.VersionAdmin):
    list_display = ('full_path', 'pub_date')


admin.site.register(Topic, TopicAdmin)

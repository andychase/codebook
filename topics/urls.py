from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(about|terms|privacy)$', views.about, name='about'),
    url(r'^(.*)', views.get_topic, name='get_topic'),
]
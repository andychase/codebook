from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

password_reset_confirm = \
 "^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # User authentication
    url(r'^login/$', views.login_view, name='login'),
    url(r'^create_account/$', views.create_account_view, name='create_account'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^password_reset/$', views.password_reset_view, name='password_reset'),
    url(password_reset_confirm, auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),

    # About
    url(r'^about/(about|terms|privacy)$', views.about, name='about'),
    # Topics
    url(r'^topics/(.*)', views.get_topic, name='get_topic'),
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from topics.views import sso
from .views import users
from .views import topics

urlpatterns = [
    # User authentication
    url(r'^_login/$', users.login_view, name='login'),
    url(r'^_login/sso$', sso.sso),
    url(r'^_accounts/login/$', users.login_view, name='login'),
    url(r'^_create_account/$', users.create_account_view, name='create_account'),
    url(r'^_logout/$', users.logout_view, name='logout'),
    url(r'^_reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # Topics
    url(r'^_tag/$', topics.tag_topic, name='tag_topic'),
    url(r'^_icon/([0-9]+)\.ico$', topics.get_link_icon, name='get_link_icon'),
    url(r'^(.*)/$', topics.get_topic, name='get_topic'),
    url(r'^()$', topics.get_topic, name='get_topic'),
]

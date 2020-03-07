from django.urls import re_path
from django.contrib.auth import views as auth_views

from topics.views import sso
from .views import users
from .views import topics

app_name = 'topics'

urlpatterns = [
    # User authentication
    re_path(r'^_login/$', users.login_view, name='login'),
    re_path(r'^_login/sso$', sso.sso),
    re_path(r'^_accounts/login/$', users.login_view, name='login'),
    re_path(r'^_create_account/$', users.create_account_view, name='create_account'),
    re_path(r'^_logout/$', users.logout_view, name='logout'),
    re_path(r'^_reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    # Topics
    re_path(r'^_tag/$', topics.tag_topic, name='tag_topic'),
    re_path(r'^_icon/([0-9]+)\.ico$', topics.get_link_icon, name='get_link_icon'),
    re_path(r'^(.*)/$', topics.get_topic, name='get_topic'),
    re_path(r'^()$', topics.get_topic, name='get_topic'),
]

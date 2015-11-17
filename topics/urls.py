from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import users
from .views import topics
from .views import topics_new
from .views import home_about

password_reset_confirm = \
    "^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$"

urlpatterns = [
    # User authentication
    url(r'^_login/$', users.login_view, name='login'),
    url(r'^_accounts/login/$', users.login_view, name='login'),
    url(r'^_create_account/$', users.create_account_view, name='create_account'),
    url(r'^_logout/$', users.logout_view, name='logout'),
    url(r'^_password_reset/$', users.password_reset_view, name='password_reset'),
    url(password_reset_confirm, auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^_password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^_reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # About
    url(r'^_about/(about|terms|privacy)$', home_about.about, name='about'),
    # Topics
    url(r'^(.*)_new/$', topics_new.new_topic, name='new_topic'),
    # url(r'^(.*)/_edit/$', topics.get_topic, name='edit_topic'),
    # url(r'^(.*)/_history/$', topics.get_topic, name='history_topic'),
    url(r'^(.*)/$', topics.get_topic, name='get_topic'),
]

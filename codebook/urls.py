"""codebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView
from codebook import settings
from topics.views import users
from django.contrib.auth import views as auth_views

password_reset_confirm = \
    "^_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$"

urlpatterns = [
                  url(r'^_admin/', include(admin.site.urls)),
                  url(r'^_password_reset/$', users.password_reset_view, name='password_reset'),
                  url(password_reset_confirm, auth_views.password_reset_confirm, name='password_reset_confirm'),
                  url(r'^_password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
                  url(r'^favicon.ico$',
                      RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=False)),
                  url(r'', include('topics.urls', namespace='topics')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

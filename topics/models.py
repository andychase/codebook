import urllib.parse
from io import StringIO

import lxml
import lxml.html
import requests
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.datetime_safe import datetime
import reversion as revisions
import django.utils.text

from topics.helpers.view_helpers import normalize_url


class BadTopicPath(Exception):
    pass


def validate_topic_name(name):
    if len(name) < 1:
        raise ValidationError('Topic name must be at least 1 character')
    elif name.lower()[0] == '_':
        raise ValidationError('Topic name cannot start with an underscore')


@revisions.register
class TopicSite(Site):
    header = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=120, blank=True)
    allow_anonymous_edits = models.BooleanField(default=True)
    create_date = models.DateTimeField('date created', default=datetime.now)
    users = models.ManyToManyField(User)
    admin = models.ForeignKey(User, null=True, blank=True, related_name="admin_user")

    def __str__(self):
        return self.name

    @staticmethod
    def get_from_name(name):
        results = Site.objects.values('id', 'name').filter(name=name)
        for result in results:
            return result['id']

    @staticmethod
    def get_from_request(request):
        try:
            return TopicSite.objects.filter(site_ptr_id=get_current_site(request)).first()
        except ObjectDoesNotExist:
            return None

    def can_user_edit(self, user_id):
        return self.allow_anonymous_edits or self.users.filter(id=user_id).count() > 0

    def is_user_admin(self, user):
        return self.admin == user


class TopicSiteData(Site):
    css_style = models.TextField(blank=True)

    @classmethod
    def get_css_style(cls, site_id):
        site = cls.objects.filter(site_ptr_id=site_id).values('css_style').first()
        if site:
            return site['css_style']
        else:
            return ""

    @classmethod
    def update_css_style(cls, site_id, stylesheet):
        site = cls.objects.filter(site_ptr_id=site_id).first()
        if site:
            site.css_style = stylesheet
            site.save()
        else:
            cls(site_ptr_id=site_id, css_style=stylesheet).save()


class Tag(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField()
    slug = models.TextField(unique=True)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.text

    def clean(self):
        self.text = self.text.strip().lower()
        self.slug = django.utils.text.slugify(self.text)

    @staticmethod
    def save_tags(link_id, tag_text_list, user):
        link = Link.objects.get(pk=link_id)
        for tag_text in tag_text_list:
            tag = Tag(text=tag_text, user=user)
            tag.clean()
            tag.save()
            link.tags.add(tag)


class Link(models.Model):
    user = models.ForeignKey(User)
    link = models.TextField(unique=True)
    title = models.TextField()
    icon = models.TextField(blank=True)
    site = models.ForeignKey(Site)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_links(current_site, tags):
        if any(tags):
            return Link.objects.filter(site_id=current_site, tags__slug__in=tags).select_related()
        else:
            return Link.objects.filter(site_id=current_site).select_related()

    @staticmethod
    def save_link(url, user, site):
        # Fix url
        url_raw = url
        if not url_raw.startswith('http'):
            url_raw = 'http://' + url_raw
        url = urllib.parse.urlparse(url_raw)
        url_full = normalize_url(url)

        # Parse title & icon
        page = requests.get(url_full)
        parsed = lxml.html.parse(StringIO(page.text))
        title = parsed.find(".//title").text
        icon = None
        icon_node = parsed.xpath('.//link[contains(@rel, "icon")]')
        if icon_node:
            icon = icon_node[0].attrib.get("href")
            icon = normalize_url(urllib.parse.urlparse(icon), url.netloc)
        if not icon:
            icon = "{}://{}/favicon.ico".format(url.scheme, url.netloc)

        link = Link(
                link=url_full,
                title=title,
                icon=icon,
                user=user,
                site=site
        )
        link.save()

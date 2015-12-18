from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.datetime_safe import datetime
import reversion as revisions
import django.utils.text


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


class Link(models.Model):
    user = models.ForeignKey(User)
    link = models.TextField()
    title = models.TextField()
    site = models.ForeignKey(Site)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    @staticmethod
    def get_all_links(current_site):
        return Link.objects.filter(site_id=current_site)


class Tags(models.Model):
    ip = models.TextField()
    user = models.ForeignKey(User)
    text = models.TextField(unique=True)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    def clean(self):
        self.text = django.utils.text.slugify(self.text)


class LinkVotes(models.Model):
    ip = models.TextField()
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    class Meta:
        unique_together = (("user", "link"),)


class TagVotes(models.Model):
    ip = models.TextField()
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Link)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    class Meta:
        unique_together = (("user", "tag"),)

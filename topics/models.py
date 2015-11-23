from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.datetime_safe import datetime
import reversion as revisions


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


@revisions.register
class Topic(models.Model):
    orig_name = models.CharField(max_length=120, validators=[validate_topic_name])
    name = models.CharField(max_length=120, blank=True, validators=[validate_topic_name])
    active = models.BooleanField(default=True)
    text = models.TextField(blank=True)
    site = models.ForeignKey(Site)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('Topic', blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    class Meta:
        unique_together = (("site", "parent", "name"),)

    def __str__(self):
        path = self.full_path()
        if path:
            return path
        else:
            return "<root>"

    @staticmethod
    def clean_name(orig_name):
        return orig_name.lower().replace(" ", "-").replace("/", "-")

    def clean(self):
        self.name = self.clean_name(self.orig_name)

    def full_path(self):
        parent_path = self.parent.full_path() + "/" if self.parent else ""
        return parent_path + self.name

    def full_path_ids(self, child_ids=tuple()):
        if self.parent:
            return self.parent.full_path_ids((self.id,) + child_ids)
        else:
            return (self.id,) + child_ids

    def any_children(self):
        return Topic.objects.filter(parent=self.id, active=True).count() > 0

    @staticmethod
    def get_from_id(topic_id):
        return Topic.objects.get(id=topic_id)

    @classmethod
    def get_deleted(cls, orig_name, parent_id, site):
        return Topic.objects.filter(name=cls.clean_name(orig_name), parent_id=parent_id, site_id=site.id, active=False)

    @staticmethod
    def get_from_path(site_id, path, parent_id=None):
        if len(path) == 1:
            results = Topic.objects.values('id', 'name', 'parent', 'site')
            results = results.filter(
                name__iexact=path[0],
                parent=parent_id,
                site=site_id,
                active=True
            ).order_by("order", "id")
            for result in results:
                return result
        else:
            results = Topic.objects.values('id', 'name', 'parent', 'site')
            results = results.filter(
                name__iexact=path[0],
                parent=parent_id,
                site=site_id,
                active=True
            ).order_by("order", "id")
            for result in results:
                return Topic.get_from_path(site_id, path[1:], result['id'])
        raise BadTopicPath

    @staticmethod
    def get_siblings(parent_id):
        results = Topic.objects.values('id', 'orig_name', 'name', 'parent')
        results = results.filter(parent=parent_id, active=True).order_by("order", "id")
        return list(results)

    @staticmethod
    def get_tree_top(site_id):
        results = Topic.objects.values('id', 'orig_name', 'name', 'parent', 'site')
        results = results.filter(parent=None, active=True, site=site_id).order_by("order", "id")
        return results

    @staticmethod
    def get_topics(site_id, path, root=(), past_path=()):
        if not root:
            root = Topic.get_tree_top(site_id)
            yield root
        next_id = False
        for i in root:
            if i['name'] == path[0]:
                next_id = i['id']
        if not next_id:
            raise BadTopicPath
        next_part = Topic.get_siblings(next_id)
        for part in next_part:
            part['path'] = past_path + (path[0],) + (part['name'],)
        yield next_part
        if len(path) > 1:
            yield from Topic.get_topics(site_id, path[1:], next_part, past_path + path[:1])

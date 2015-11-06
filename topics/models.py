from django.core.exceptions import ValidationError
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
class Topic(models.Model):
    orig_name = models.CharField(max_length=120, validators=[validate_topic_name])
    name = models.CharField(max_length=120, blank=True, validators=[validate_topic_name])
    text = models.TextField(blank=True)
    parent = models.ForeignKey('Topic', blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    class Meta:
        unique_together = (("parent", "name"),)

    def __str__(self):
        return self.full_path()

    def clean(self):
        self.name = self.orig_name.lower()

    def full_path(self):
        parent_path = self.parent.full_path() + "/" if self.parent else ""
        return parent_path + self.name

    @staticmethod
    def get_from_path(path, parent_id=None):
        if len(path) == 1:
            results = Topic.objects.values('id', 'name', 'parent')
            results = results.filter(name__iexact=path[0], parent=parent_id)
            for result in results:
                return result
        else:
            results = Topic.objects.values('id', 'name', 'parent')
            results = results.filter(name__iexact=path[0], parent=parent_id)
            for result in results:
                return Topic.get_from_path(path[1:], result['id'])
        raise BadTopicPath

    @staticmethod
    def get_siblings(parent_id):
        return [i for i in Topic.objects.values('id', 'name', 'parent').filter(parent=parent_id)]

    @staticmethod
    def get_tree_top():
        results = Topic.objects.values('id', 'name', 'parent')
        results = results.filter(parent=None)
        return results

    @staticmethod
    def get_topics(path, root=(), past_path=()):
        if not root:
            root = Topic.get_tree_top()
            yield root
        next_id = False
        for i in root:
            if i['name'].lower() == path[0].lower():
                next_id = i['id']
        if not next_id:
            raise BadTopicPath
        next_part = Topic.get_siblings(next_id)
        for part in next_part:
            part['path'] = past_path + (path[0],) + (part['name'],)
        yield next_part
        if len(path) > 1:
            yield from Topic.get_topics(path[1:], next_part, past_path + path[:1])

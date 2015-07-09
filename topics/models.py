from django.db import models
from django.utils.datetime_safe import datetime


class Topic(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField(blank=True)
    parent = models.ForeignKey('Topic', blank=True)
    parent.null = True

    pub_date = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.full_path()

    def full_path(self):
        parent_path = self.parent.full_path() + "/" if self.parent else ""
        return parent_path + self.name

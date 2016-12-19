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
from django.db.models import Count
from django.utils import timezone
import django.utils.text
from requests.exceptions import ReadTimeout

from topics.helpers.view_helpers import normalize_url


class BadTopicPath(Exception):
    pass


def validate_topic_name(name):
    if len(name) < 1:
        raise ValidationError('Topic name must be at least 1 character')
    elif name.lower()[0] == '_':
        raise ValidationError('Topic name cannot start with an underscore')


class TopicSite(Site):
    header = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=120, blank=True)
    allow_anonymous_edits = models.BooleanField(default=True)
    create_date = models.DateTimeField('date created', default=timezone.now)
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


class Source(models.Model):
    name = models.TextField()
    site = models.TextField()

    def clean(self):
        self.text = self.text.strip()
        self.slug = django.utils.text.slugify(self.text)


class Tag(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField()
    slug = models.TextField(unique=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.text

    def clean(self):
        self.text = self.text.strip().lower()
        self.slug = django.utils.text.slugify(self.text)

    @staticmethod
    def delete_tag(tag_name):
        tag = Tag.objects.filter(text=tag_name).first()
        if tag:
            tag.delete()

    @staticmethod
    def save_tags(link_id, tag_text_list, user):
        link = Link.objects.get(pk=link_id)
        for tag_text in tag_text_list:
            if not tag_text:
                continue
            slug = django.utils.text.slugify(tag_text)
            previous = Tag.objects.filter(slug=slug).first()
            if previous:
                tag = previous
            else:
                tag = Tag(text=tag_text, user=user)
                tag.clean()
                tag.save()
            link.tags.add(tag)

    @staticmethod
    def _filter_duplicates(q, site, selected_tags):
        """
        This function goes through each tag and re-ranks and filters them,
        prioritizing tags that contain links that haven't been listed in another tag higher.

        Also filters tags that have all links fully contained in other tags.
        """
        q = list(q[:20])
        seen_links = set()
        for tag in q:
            if tag['tag__slug'] not in selected_tags:
                for link in Link.get_all_links(site, selected_tags + [tag['tag__slug']]).values('link'):
                    if link['link'] in seen_links:
                        tag['number_of_links'] -= 1
                    else:
                        seen_links.add(link['link'])

        q.sort(key=lambda _: _['number_of_links'], reverse=True)
        q = [t for t in q if t['number_of_links'] > 0]
        return q

    @staticmethod
    def get_top_tags(site, tags):
        q = (
            Link.tags.through.objects
                .values('tag')
                .annotate(number_of_links=Count('link'))
                .values('tag', 'number_of_links', 'tag__text', 'tag__slug')
                .order_by('-number_of_links')
        )
        if any(tags):
            q = q.filter(link__in=Link.get_all_links(site, tags))
            q = Tag._filter_duplicates(q, site, tags)

        return q[:10]

    @staticmethod
    def get_top_tag_list(site, selected_tags):
        def fix_tags(tags, sel=None):
            for tag in tags:
                tag['path'] = [tag['tag__slug']]
                tag['slug'] = tag['tag__slug']
                tag['text'] = tag['tag__text']
                if any(selected_tags) and sel is not None and sel < len(selected_tags):
                    if selected_tags[sel] == tag['slug']:
                        tag['active'] = True
            if any(selected_tags) and sel is not None and sel <= len(selected_tags):
                tags = [tag for tag in tags if tag['slug'] not in selected_tags[:sel]]
            return tags

        def add_tag_path(path, tags):
            for tag in tags:
                tag['path'] = path + [tag['tag__slug']]

        # Base Nav
        output_tags = Tag.get_top_tags(site, [])
        output_tags = fix_tags(output_tags, 0)
        yield output_tags
        # noinspection PyArgumentList
        for i in range(1, len(selected_tags) + 1):
            output_tags = Tag.get_top_tags(site, selected_tags[:i])
            output_tags = fix_tags(output_tags, i)
            add_tag_path(selected_tags[:i], output_tags)
            yield output_tags


class Link(models.Model):
    user = models.ForeignKey(User)
    link = models.TextField(unique=True)
    title = models.TextField(blank=True)
    icon = models.TextField(blank=True)
    icon_data = models.BinaryField(blank=True, null=True)
    icon_content_type = models.TextField(blank=True)
    type = models.TextField(blank=True)
    rating_difficulty = models.IntegerField(null=True, blank=True)
    rating_quality = models.IntegerField(null=True, blank=True)
    site = models.ForeignKey(Site)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_links(current_site, tags):
        q = Link.objects.filter(site_id=current_site).defer('icon_data', 'icon_content_type').prefetch_related()
        if any(tags):
            for tag in tags:
                q = q.filter(tags__slug=tag)
        return q

    @staticmethod
    def get_no_tag_link(current_site):
        return (
            Link.objects
                .annotate(number_of_links=Count('tags'))
                .filter(site_id=current_site, number_of_links=0)
                .first()
        )

    @staticmethod
    def delete_link(link_id):
        link = Link.objects.get(pk=link_id)
        link.delete()

    @staticmethod
    def rename_link(link_id, title):
        link = Link.objects.get(pk=link_id)
        link.title = title
        link.clean()
        link.save()

    @staticmethod
    def save_ratings(link_id, link_type, link_difficulty, link_quality):
        if (link_type, link_difficulty, link_quality) != (None, None, None):
            link = Link.objects.get(pk=link_id)
            if link_type is not None:
                link.type = link_type
            if link_difficulty is not None:
                link.rating_difficulty = int(link_difficulty)
            if link_quality is not None:
                link.rating_quality = int(link_quality)

            link.save()

    @staticmethod
    def save_link(url, user, site):
        # Fix url
        url_raw = url
        if not url_raw.startswith('http'):
            url_raw = 'http://' + url_raw
        url = urllib.parse.urlparse(url_raw)
        url_full = normalize_url(url)

        previous_link = Link.objects.filter(link=url_full).first()
        if previous_link:
            link = previous_link
        else:
            link = Link(link=url_full, user=user, site=site)

        # Parse title & icon
        page = requests.get(url_full, timeout=1)
        parsed = lxml.html.parse(StringIO(page.text))
        title = "<UNK>"
        title_node = parsed.find(".//title")
        if title_node is not None:
            title = title_node.text
        icon = None
        icon_node = parsed.xpath('.//link[contains(@rel, "icon")]')
        if icon_node:
            icon = icon_node[0].attrib.get("href")
            icon = normalize_url(urllib.parse.urlparse(icon), url.netloc)
        if not icon:
            icon = "{}://{}/favicon.ico".format(url.scheme, url.netloc)
        try:
            if requests.get(icon, timeout=1).status_code != 200:
                icon = ""
        except ReadTimeout:
            icon = ""

        # Save Link
        link.icon = icon
        link.save_icon_data()
        if not link.title and title:
            link.title = title
        link.save()

    def save_icon_data(self):
        if self.icon and not self.icon_data:
            try:
                request = requests.get(self.icon)
                if request.headers.startswith('text/html') or request.headers.startswith('text/plain'):
                    return
                self.icon_content_type = request.headers['content-type']
                self.icon_data = request.content
                self.save()
            except ReadTimeout:
                pass

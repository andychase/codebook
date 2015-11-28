import json
import re
from typing import Dict, List
from urllib.parse import urlparse
import markdown
from django.template.defaultfilters import register
from django.utils import safestring
import html

from topics.helpers.allowed_icons import allowed_icons

tag_detector = re.compile("#([a-zA-Z]+[A-Za-z0-9]*)")
tag_markup = """
<span class="tag"><span class="hash">#</span><span class="name">\g<1></span></span>
""".strip()


def detect_tags(text):
    return tag_detector.findall(text)


def add_tags_to_topic_resources(resources: List[Dict[str, Dict[str, str]]]) -> None:
    for resource in resources:
        if resource.get("link"):
            resource['link']['tags'] = detect_tags(resource['link'].get("metadata", ""))
            if any(resource['link']['tags']):
                if resource['link']['tags'][-1] in allowed_icons:
                    resource['link']['icon'] = resource['link']['tags'][-1]


def replace_tags(text):
    return tag_detector.sub(tag_markup, text)


def setup():
    @register.filter(name='markdownify')
    def markdownify(value):
        return safestring.mark_safe(markdown.markdown(replace_tags(value)))

    @register.filter(name='un_markdownify')
    def un_markdownify(value):
        return safestring.mark_safe(html.unescape(value)).replace('"', "&quot;")

    @register.filter(name='get_item')
    def get_item(dictionary, key):
        return dictionary.get(key)


duplicate_topic_warning = """
<i class="ss-alert"></i>
There was an error while renaming or rearranging topics:
a topic with that name already exists in this category.
"""


def www_remover(input_text, r=re.compile("^www\.")):
    return r.sub("", input_text)


def url_handler(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    output_url = parsed.geturl()
    domain = www_remover(parsed.netloc)
    domain_link = "{}://{}".format(parsed.scheme, domain)
    return domain, domain_link, output_url


def process(input_string) -> List[Dict[str, Dict[str, str]]]:
    if any(input_string.strip()):
        data = json.loads(input_string)
        for item in data:
            for data_type, d in item.items():
                if data_type == "link":
                    d['url'] = url_handler(d['url'])
        return data
    else:
        return []


def add_active_to_topic_path(topics, nav_active):
    for i, active, topic_list in zip(range(1, len(topics) + 1), nav_active, topics):
        for topic in topic_list:
            if topic['name'] == active:
                topic['active'] = True
            if i == len(nav_active):
                topic['last_nav'] = True


def topic_name_to_path(topic_name):
    topic_name = topic_name[:2000]
    topic_path = tuple(topic_name.strip("/").split("/"))
    topic_path_is_root = (topic_path == ("",))
    return topic_path, topic_path_is_root

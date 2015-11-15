import json
import re
from urllib.parse import urlparse

import markdown
from django.template.defaultfilters import register
from django.utils import safestring


def setup():
    @register.filter(name='markdownify')
    def markdownify(value):
        return safestring.mark_safe(markdown.markdown(value))

    @register.filter(name='un_markdownify')
    def un_markdownify(value):
        return safestring.mark_safe(value)

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


def process(input_string):
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

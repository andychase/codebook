from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.views.decorators.cache import cache_page

DEFAULT_TIMEOUT = 60 * 24


def make_cache_key(site_domain, topic_name):
    return ":".join((site_domain, topic_name))


def special_page_in_path(topic_name):
    return max(len(i) > 0 and i[0] == "_" for i in topic_name.split("/"))


def clear_topic(site_domain, topic_name):
    cache.delete(make_cache_key(site_domain, topic_name))


def clear_site(site_domain):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(make_cache_key(site_domain, "*"))
    else:
        cache.clear()


def cache_topic(func):
    def show_topic(request, topic_name, retry=False):
        if request.user.is_authenticated() or special_page_in_path(topic_name):
            return func(request, topic_name, retry)
        cache_key = make_cache_key(get_current_site(request).domain, topic_name)
        existing_cache = cache.get(cache_key)
        if existing_cache:
            return existing_cache
        else:
            response = func(request, topic_name, retry)
            if hasattr(response, 'render') and callable(response.render):
                response.add_post_render_callback(
                    lambda r: cache.set(cache_key, r, DEFAULT_TIMEOUT)
                )
            else:
                cache.set(cache_key, response, DEFAULT_TIMEOUT)
            return response

    return show_topic

from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

DEFAULT_TIMEOUT = 60 * 24


def make_cache_key(site_domain, topic_name):
    return ":".join((site_domain, topic_name))


def special_page_in_path(topic_name):
    return max(len(i) > 0 and i[0] == "_" for i in topic_name.split("/"))


def should_cache(request):
    return (
        'sessionid' not in request.COOKIES and
        not special_page_in_path(request.get_full_path()) and
        'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', [])
    )


def clear_topic(site_domain, topic_name):
    cache.delete(make_cache_key(site_domain, topic_name))


def clear_site(site_domain):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(make_cache_key(site_domain, "*"))
    else:
        cache.clear()


class TopicCacheMiddleware:
    def process_request(self, request):
        if should_cache(request):
            cache_key = make_cache_key(get_current_site(request).domain, request.get_full_path())
            existing_cache = cache.get(cache_key)
            if existing_cache:
                return existing_cache

    def process_response(self, request, response):
        if should_cache(request):
            cache_key = make_cache_key(get_current_site(request).domain, request.get_full_path())
            if hasattr(response, 'render') and callable(response.render):
                response.add_post_render_callback(
                    lambda r: cache.set(cache_key, r, DEFAULT_TIMEOUT)
                )
            else:
                cache.set(cache_key, response, DEFAULT_TIMEOUT)
        return response

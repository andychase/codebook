from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

DEFAULT_TIMEOUT = 60 * 24


def make_cache_key(site_domain, topic_name):
    return ":".join((site_domain, topic_name))


def special_page_in_path(topic_name):
    return max(len(i) > 0 and i[0] == "_" for i in topic_name.strip("/").split("/"))


def should_cache_request(request, path):
    return (
        'sessionid' not in request.COOKIES and
        not special_page_in_path(path) and
        'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', [])
    )


def should_cache_response(response):
    return (
        response.status_code == 200 and not response.streaming
    )


def clear_topic(site_domain, topic_name):
    cache.delete(make_cache_key(site_domain, topic_name.strip("/")))


def clear_site(site_domain):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(make_cache_key(site_domain, "*"))
    else:
        cache.clear()


class TopicCacheMiddleware:
    def process_request(self, request):
        path = request.get_full_path().strip("/")
        if should_cache_request(request, path):
            cache_key = make_cache_key(get_current_site(request).domain, path)
            existing_cache = cache.get(cache_key)
            if existing_cache:
                return existing_cache

    def process_response(self, request, response):
        path = request.get_full_path().strip("/")
        if should_cache_request(request, path) and should_cache_response(response):
            cache_key = make_cache_key(get_current_site(request).domain, path)
            if hasattr(response, 'render') and callable(response.render):
                response.add_post_render_callback(
                    lambda r: cache.set(cache_key, r, DEFAULT_TIMEOUT)
                )
            else:
                cache.set(cache_key, response, DEFAULT_TIMEOUT)
        return response

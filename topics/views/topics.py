from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template import loader, RequestContext

from topics.helpers import view_helpers
from topics.models import Link

view_helpers.setup()


def get_topic(request, _,):
    if request.POST:
        pass
    else:
        template = loader.get_template('topics/show_topic.html')
        context = RequestContext(request, {
            'links': Link.get_all_links(get_current_site(request).id),
        })
        return HttpResponse(template.render(context))

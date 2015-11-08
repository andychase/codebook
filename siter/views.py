from django.http import HttpResponse
from django.template import loader, RequestContext


def site_not_found(request, path):
    template = loader.get_template('siter/site_not_found.html')
    context = RequestContext(request, {
        'path': path
    })
    return HttpResponse(template.render(context))

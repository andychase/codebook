from django.contrib.auth import logout
from django.contrib.auth import views
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect

from topics.settings_context import settings_context


def create_account_view(_):
    return HttpResponseForbidden()


def login_view(request):
    extra_context = {
        'next': request.GET.get("next"),
        'fromlink': True if request.GET.get("fromlink") == 'true' else False
    }
    extra_context.update(settings_context(request))
    template_response = views.login(request, extra_context=extra_context)
    return template_response


def password_reset_view(request):
    extra_context = {
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def password_reset_confirm_view(request):
    extra_context = {
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def logout_view(request):
    if request.POST:
        next_link = "." if not request.POST.get("next") else request.POST.get("next")
        logout(request)
        return redirect(next_link)

    raise Http404("Logout must be called from the link on the website, not directly")

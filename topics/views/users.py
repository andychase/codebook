from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.contrib.auth import views
from django.shortcuts import redirect
from django.template import loader, RequestContext

from siter.views import site_not_found
from topics.models import Topic
from topics.settings_context import settings_context


def catch_site_not_found(func):
    def protected_func(request):
        try:
            topics = [Topic.get_tree_top(get_current_site(request))]
            return func(request, topics)
        except ObjectDoesNotExist:
            return site_not_found(request, "")

    return protected_func


@catch_site_not_found
def create_account_view(request, topics):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.data['username'], password=form.data['password1'])
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    template = loader.get_template('registration/create_account.html')
    context = RequestContext(request, {
        'topics': topics,
        'form': form
    })
    return HttpResponse(template.render(context))


@catch_site_not_found
def login_view(request, topics):
    extra_context = {
        'topics': topics,
        'next': request.GET.get("next"),
        'fromlink': True if request.GET.get("fromlink") == 'true' else False
    }
    extra_context.update(settings_context(request))
    template_response = views.login(request, extra_context=extra_context)
    return template_response


@catch_site_not_found
def password_reset_view(request, topics):
    extra_context = {
        'topics': topics,
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


@catch_site_not_found
def password_reset_confirm_view(request, topics):
    extra_context = {
        'topics': topics,
    }
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def logout_view(request):
    if request.POST:
        next_link = "." if not request.POST.get("next") else request.POST.get("next")
        logout(request)
        return redirect(next_link)

    raise Http404("Logout must be called from the link on the website, not directly")

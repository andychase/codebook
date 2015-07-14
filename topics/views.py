from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404
from django.contrib.auth import views
from django.shortcuts import redirect
from django.template import loader, RequestContext
from django.template.defaultfilters import register
from django.utils import safestring
import markdown
import yaml

from topics.models import Topic
from topics.parser import process


with open('./topics/config.yml') as f:
    site = yaml.safe_load(f)


def default_context_variables(variables, request=None):
    default_vars = {
        'site': site,
    }
    if request is not None:
        default_vars['user'] = request.user
    default_vars.update(variables)
    return default_vars


def default_context(request, variables):
    return RequestContext(request, default_context_variables(variables, request))


@register.filter(name='markdownify')
def cut(value):
    return safestring.mark_safe(markdown.markdown(value))


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def about(request, info_page_title):
    if info_page_title not in ['privacy', 'terms']:
        info_page_title = "about"
    with open('./topics/info/{}.md'.format(info_page_title)) as f:
        page_content = markdown.markdown(f.read())

    template = loader.get_template('layouts/page.html')
    context = default_context(request, {
        'content': safestring.mark_safe(page_content),
        'topics': [Topic.get_tree_top()],
        'title': info_page_title
    })
    return HttpResponse(template.render(context))


def index(request):
    template = loader.get_template('index.html')
    context = default_context(request, {
        'topics': [Topic.get_tree_top()]
    })
    return HttpResponse(template.render(context))


def topic_data_to_stream(topic_data):
    current_section = ""
    current_subsection = ""
    if not topic_data:
        return []
    for (_, link_block, _) in topic_data:
        if link_block:
            if link_block['section'] != current_section:
                current_section = link_block['section']
                current_subsection = ""
                yield {'section': current_section}
            if link_block['subsection'] != current_subsection:
                current_subsection = link_block['subsection']
                yield {'subsection': current_subsection}
            link_block['authors'] = [safestring.mark_safe(a) for a in link_block['authors']]
            yield {'link': link_block}


def get_topic(request, topic_name):
    topic_name = topic_name[:50]
    topic_path = tuple(topic_name.strip("/").split("/"))
    topics = list(Topic.get_topics(topic_path))
    topic_id = None
    for topic in topics[-2]:
        if topic['name'].lower() == topic_path[-1].lower():
            topic_id = topic['id']

    template = loader.get_template('layouts/topic.html')
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    topic_data = topic_data_to_stream(process(topic.text))
    context = default_context(request, {
        'topics': topics,
        'nav_active': topic_path,
        'resources': topic_data
    })
    return HttpResponse(template.render(context))


# Accounts

def create_account_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.data['username'], password=form.data['password1'])
            login(request, user)
            redirect('index')
    else:
        form = UserCreationForm()

    template = loader.get_template('registration/create_account.html')
    context = default_context(request, {
        'topics': [Topic.get_tree_top()],
        'form': form
    })
    return HttpResponse(template.render(context))


def login_view(request):
    extra_context = default_context_variables({
        'topics': [Topic.get_tree_top()],
    })
    template_response = views.login(request, extra_context=extra_context)
    return template_response


def password_reset_view(request):
    extra_context = default_context_variables({
        'topics': [Topic.get_tree_top()],
    })
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def password_reset_confirm_view(request):
    extra_context = default_context_variables({
        'topics': [Topic.get_tree_top()],
    })
    template_response = views.password_reset(request, extra_context=extra_context)
    return template_response


def logout_view(request):
    logout(request)
    return redirect('index')

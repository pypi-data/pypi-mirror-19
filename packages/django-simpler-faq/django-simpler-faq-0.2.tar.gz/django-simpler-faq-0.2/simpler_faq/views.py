from django.views.generic import ListView

from .models import Topic


class Topics(ListView):
    template_name = 'simpler_faq/topic_list.html'
    context_object_name = 'topics'
    model = Topic

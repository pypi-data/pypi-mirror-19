#! coding: utf-8
from django.conf.urls import url

from .views import Topics


urlpatterns = [
    url(r'^', Topics.as_view(), name='faq'),
]

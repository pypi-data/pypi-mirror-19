#! coding: utf-8
from django.contrib import admin
from .models import Topic, Question


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'order')
    list_editable = ('order',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'topic', 'order')
    list_editable = ('topic', 'order',)
    list_filter = ('topic',)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)

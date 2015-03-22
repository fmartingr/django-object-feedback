# coding: utf-8

# django
from django.contrib import admin

# app
from .models import ObjectFeedback


class FeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(ObjectFeedback, FeedbackAdmin)

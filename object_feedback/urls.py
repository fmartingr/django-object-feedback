# coding: utf-8

# django
from django.conf.urls import patterns, url

# app
from .views import ObjectFeedbackView, FeedbackView

urlpatterns = patterns(
    '',
    url(r'^(?P<ct_pk>\d+)/(?P<obj_pk>\d+)/$',
        ObjectFeedbackView.as_view(),
        name="object"),
    url(r'^$',
        FeedbackView.as_view(),
        name="general"),
)

from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from sentenceDetection import views
from .old_api import  sd_view

urlpatterns = [
    path('', views.SentenceDetection.as_view()),
    path('old',sd_view.SentenceDetectionAPI.as_view()),
]
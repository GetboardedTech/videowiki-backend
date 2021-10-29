from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from summarization import views,summerizer

urlpatterns = [
    path('', views.Summarization.as_view()),
    path('new', summerizer.Summarization.as_view())
]
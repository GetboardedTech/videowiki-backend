from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from videoSearch import views,vs_api

urlpatterns = [
    path('old', views.videoSearch.as_view()),
    path('',vs_api.VideoSearchAPI.as_view())
]
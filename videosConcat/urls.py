from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from videosConcat import views

urlpatterns = [
    path('', views.VideoPreviewMaker.as_view())
]
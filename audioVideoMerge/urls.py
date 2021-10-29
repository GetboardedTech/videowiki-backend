from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from audioVideoMerge import views

urlpatterns = [
    path('', views.AudioVideoMerge.as_view())
]
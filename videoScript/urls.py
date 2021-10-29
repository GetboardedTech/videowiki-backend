from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from videoScript import views

urlpatterns = [
    path('', views.videoScript.as_view())
]
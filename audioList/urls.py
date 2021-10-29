from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from audioList import views

urlpatterns = [
    path('', views.AudioList.as_view())
]
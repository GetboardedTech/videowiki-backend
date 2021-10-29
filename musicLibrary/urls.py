from django.contrib import admin
from django.urls import path

from musicLibrary import views

urlpatterns = [
    path('music', views.MusicList.as_view())
]

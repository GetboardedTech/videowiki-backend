from django.contrib import admin
from django.urls import path


from videoList import vl_api

urlpatterns = [
    path('', vl_api.VideoList.as_view())
]
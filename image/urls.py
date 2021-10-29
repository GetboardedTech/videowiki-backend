from django.contrib import admin
from django.urls import path


from image import views

urlpatterns = [
    path('zoom', views.ImageVideo.as_view()),
]
from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from keywordExtraction import views,ke_api,tag_suggestor

urlpatterns = [
    path('old', views.KeywordExtraction.as_view()),
    path('', ke_api.KeywordExtraction.as_view()),
    path('tags',tag_suggestor.TagFinder.as_view())
]
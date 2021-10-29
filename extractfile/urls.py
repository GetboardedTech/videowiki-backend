from django.urls import path, include
from extractfile.views import ExtractDetailFromUrl, ExtractDetailFromFile


urlpatterns = [
    path(r'extract_info_url', ExtractDetailFromUrl.as_view()),
    path(r'extract_info_file', ExtractDetailFromFile.as_view())
]


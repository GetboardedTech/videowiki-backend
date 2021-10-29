from django.urls import path, include
from .views import caption, video_chunks, sil_vid

urlpatterns = [
    path('caption/', caption.as_view()),
    path('video-chunks/', video_chunks.as_view()),
    path('silence/', sil_vid.as_view())
]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sd/', include('sentenceDetection.urls')),
    path('ke/', include('keywordExtraction.urls')),
    path('vl/', include('videoList.urls')),
    path('vs/', include('videoSearch.urls')),
    path('al/', include('audioList.urls')),
    path('smz/', include('summarization.urls')),

    path('vc/', include('videosConcat.urls')),
    path('vsrt/', include('videoScript.urls')),
    path('avm/', include('audioVideoMerge.urls')),
    path('transaction/', include('transaction.urls')),
    path('api/', include('extractfile.urls')),
    path('api/', include('musicLibrary.urls')),
    path('api/',include('videoEditor.urls')),

    # for customize user
    path('api/', include('user.urls')),
    path('videoapi/', include('videos.urls')),

    #for image
    path('image/', include('image.urls')),
    # authentication
    path('api/auth/login/', obtain_jwt_token),
    path('api/auth/refresh-token/', refresh_jwt_token),
    path('api/auth/verify-token/', verify_jwt_token),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

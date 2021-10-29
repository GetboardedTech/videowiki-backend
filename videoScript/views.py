from rest_framework.views import APIView
from .video_text_merge import merger
class videoScript(APIView):
    def post(self, request):
        return merger(request)
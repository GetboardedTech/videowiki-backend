from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .music_listing_api import audioList

class AudioList(APIView):
	def post(self, request):
		return audioList(request.data["keywords"])

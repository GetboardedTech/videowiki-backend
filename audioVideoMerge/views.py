from rest_framework.views import APIView
from .audio_video_merge import merger

class AudioVideoMerge(APIView):
	def post(self,request):
		data={
			"audio":request.data["audio"],
			"video":request.data["video"],
		}
		return merger(data)


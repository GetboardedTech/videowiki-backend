from rest_framework.views import APIView
from .recognise_txt import video_to_txt
from .silence_vid import aud_url
from rest_framework import status
import requests
from django_q.tasks import async_task,result
from django.http import JsonResponse
import uuid
import os

from coutoEditor.global_variable import BASE_URL, BASE_DIR


class caption(APIView):

	def post(self, request):
		video_url = request.data['video_url']
		filename = str(uuid.uuid4())
		chunk_size = 256
		combined_video_url = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp4")
		r = requests.get(video_url, stream=True)
		with open(combined_video_url,"wb") as f:
			for chunk in r.iter_content(chunk_size=chunk_size):
				f.write(chunk)
		whole_text = video_to_txt(combined_video_url)

		return JsonResponse({"data": whole_text}, status=status.HTTP_200_OK)

class video_chunks(APIView):

	def post(self, request):

		if not request.data['task_id']:
			task_id = async_task('videoEditor.clip_chunks.split_to_chunk', request.data["video_url"], request.data["option"])
			return JsonResponse({'task_id': task_id})
		else:
			id = result(request.data['task_id'])
			if id is None:
				return JsonResponse({'status': False, 'data': id})
			else:
				return JsonResponse({'status': True, 'data': id})


class sil_vid(APIView):
	def post(self, request):
		vid_url = request.data['vid_url']
		return aud_url(vid_url)




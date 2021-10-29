from rest_framework.views import APIView
import os
from django_q.tasks import async_task,result
from django.http import JsonResponse
from .concat import single_video_concat
from coutoEditor.settings import BASE_URL, BASE_DIR
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class VideoPreviewMaker(APIView):
	def post(self, request):
		if not request.data['task_id']:
			#when only one video exitsts then concat shouldn't be queued
			try:
				is_preview = request.data['isPreview']
			except KeyError:
				is_preview = 1

			if len(request.data["videos"]) == 1:
				return single_video_concat(request,is_preview,bgm_url=request.data['bgm'])

			try:
				motions = request.data['motions']
			except KeyError:
				motions = []

			task_id = async_task('videosConcat.concat.translated_concatenation', request.data['videos'],motions,is_preview, bgm_url=request.data['bgm'])
			return JsonResponse({'task_id': task_id})
		else:
			id = result(request.data['task_id'])
			if id is None:
				return JsonResponse({'status': False, 'data': id})
			else:
				return JsonResponse({'status': True, 'data': id})

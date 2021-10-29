from django.shortcuts import render

# Create your views here.

from .apps import SentencedetectionConfig

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .working_api.sentence_transform import sen_transformation
from googletrans import Translator

class SentenceDetection(APIView):

	def post(self, request):
		if request.method == 'POST':

			response_dict = {}
			sentences = {}

			text = request.data['text']
			break_type = request.data['break_type']
			sen_list = sen_transformation(text, break_type)

			for sen in sen_list:
				sentences[len(sentences)]=str(sen)

			response_dict["sentences"] = sentences
			return JsonResponse(response_dict)

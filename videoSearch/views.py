from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from googletrans import Translator

import json
import requests
import urllib.parse

class videoSearch(APIView):

	def post(self, request):
		if request.method == 'POST':
			q = str(request.data['searchQuery'])
			srcLang = str(request.data['srcLang'])
			print('*******',q)
			API_KEY = '14852807-36c181b80405f874cca74a5f7'
			c=0
			d=0
			e=0
			userId=[]
			video_dict={}
			video_dict_sub={}
			translator = Translator()
			transObj = translator.translate(q, dest='en')
			print(transObj)
			#srcLang = transObj.src
			q = transObj.text
			URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(q)
			r = requests.get(URL)
			r = r.json()
			#print("r",r)
			if r['totalHits'] > 0:
				for hit in r['hits']:
					if hit['user_id'] not in userId:
						img_url = hit['userImageURL']
						video_url = hit['videos']['medium']['url']
						tags = hit['tags']
						transObj = translator.translate(tags, dest=srcLang)
						print(transObj)
						tags = transObj.text
						current_tag = ""
						if True: #v1 not in tags:
							current_tag = q
							current_tag = current_tag+", "
							transObj = translator.translate(current_tag, dest=srcLang)
							print(transObj)
							current_tag = transObj.text
						userId.append(hit['user_id'])
						video_dict_sub[d] = [img_url,video_url,tags,current_tag]
						d+=1
						e+=1
				#e = 0
				video_dict = video_dict_sub
				#c+=1
				#video_dict_sub = {}

			return JsonResponse(video_dict)
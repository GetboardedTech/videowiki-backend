from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from .apps import VideolistConfig

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from googletrans import Translator

import json
import requests
import urllib.parse

class VideoList(APIView):

	def post(self, request):
		if request.method == 'POST':
			q = request.data['keywords']
			srcLang = request.data['srcLang']
			print('*******',q, srcLang)
			API_KEY = '14852807-36c181b80405f874cca74a5f7'
			#URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(q)
			#r = requests.get(URL)
			#print(r.json())

			c=0
			d=0
			e=0
			userId=[]
			video_dict={}
			video_dict_sub={}
			translator = Translator()
			for k,v in q.items():
				for k1,v1 in v.items():
					print("v1",v1)
					for v2 in v1.split():
						transObj = translator.translate(v2, dest='en')
						print(transObj)
						#srcLang = transObj.src
						v2 = transObj.text
						URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(v2)
						r = requests.get(URL)
						r = r.json()
						#print("r",r)
						if r['totalHits'] > 0:
							for hit in r['hits']:
								if hit['user_id'] not in userId and e < 1:
									img_url = hit['userImageURL']
									video_url = hit['videos']['tiny']['url']
									tags = hit['tags']
									print(srcLang)
									transObj = translator.translate(tags, dest=srcLang)
									print(transObj)
									#srcLang = transObj.src
									tags = transObj.text
									print(tags)
									current_tag = ""
									if True: #v1 not in tags:
										transObj = translator.translate(v1, dest=srcLang)
										#srcLang = transObj.src
										v1 = transObj.text
										current_tag = v1
										current_tag = current_tag+", "
									userId.append(hit['user_id'])
									video_dict_sub[d] = [img_url,video_url,tags,current_tag]
									d+=1
									e+=1
							e = 0
				video_dict[c] = video_dict_sub
				c+=1
				video_dict_sub = {}
				d=0 

			print(video_dict)
			return JsonResponse(video_dict)
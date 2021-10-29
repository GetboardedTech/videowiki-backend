
from django.http import JsonResponse
from rest_framework.views import APIView

import requests
import urllib.parse

class VideoList(APIView):

	def post(self, request):
		if request.method == 'POST':
			q = request.data['keywords']
			API_KEY = '14852807-36c181b80405f874cca74a5f7'
			#URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(q)
			#r = requests.get(URL)
			#print(r.json())
			c=0
			d=0
			e=0
			userId=[]
			video_dict={}
			image_dict={}
			image_dict_sub={}
			video_dict_sub={}
			for k,v in q.items():
				for v1 in v:
					URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(str(v1))
					r = requests.get(URL)
					r = r.json()
					if r['totalHits'] > 0:
						for hit in r['hits']:
							if hit['user_id'] not in userId and e < 1:
								img_url = hit['userImageURL']
								video_url = hit['videos']['tiny']['url']
								tags = hit['tags']
								if True:
									current_tag = str(v1)
									current_tag = current_tag+", "
								userId.append(hit['user_id'])
								video_dict_sub[d] = [img_url,video_url,tags,current_tag]
								d+=1
								e+=1
						e = 0
					else:
						#default links will be generated when no videos are found
						video_dict_sub[d]=["https://oldweb.dyu.edu.tw/english/design/no-video.gif","https://oldweb.dyu.edu.tw/english/design/no-video.gif","",""]
					URL = "https://pixabay.com/api/?key="+API_KEY+"&q="+urllib.parse.quote(str(v1))
					r = requests.get(URL)
					r = r.json()
					image=[]
					if r['totalHits'] > 0:
						for hit in r['hits']:
							image=[hit["largeImageURL"],hit["tags"],v1]
							break
					if len(image)!=0:
						image_dict_sub[len(image_dict_sub)]=image
				video_dict[c] = video_dict_sub
				if len(image_dict_sub)!=0:
					image_dict[len(image_dict)]=image_dict_sub
				c+=1
				video_dict_sub,image_dict_sub = {},{}
				d=0
			return JsonResponse({"videos":video_dict,"images":image_dict})

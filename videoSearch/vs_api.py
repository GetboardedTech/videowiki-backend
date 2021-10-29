from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import urllib
from translate import Translator
class VideoSearchAPI(APIView):
    def post(self,request):
        q = str(request.data['searchQuery'])
        srcLang = str(request.data['srcLang'])
        if srcLang!="en":
            q=str(Translator(from_lang=srcLang,to_lang="en").translate(q))
        API_KEY = '14852807-36c181b80405f874cca74a5f7'
        if request.data["type"]=="video":
            d = 0
            e = 0
            userId = []
            video_dict = {}
            video_dict_sub = {}
            URL = "https://pixabay.com/api/videos/?key=" + API_KEY + "&q=" + urllib.parse.quote(q)
            r = requests.get(URL)
            r = r.json()
            if r['totalHits'] > 0:
                for hit in r['hits']:
                    if hit['user_id'] not in userId:
                        img_url = hit['userImageURL']
                        video_url = hit['videos']['tiny']['url']
                        tags = hit['tags']
                        if True:  # v1 not in tags:
                            current_tag = q
                            current_tag = current_tag + ", "
                        userId.append(hit['user_id'])
                        video_dict_sub[d] = [img_url, video_url, tags, current_tag]
                        d += 1
                        e += 1
                video_dict = video_dict_sub
            return Response(video_dict)
        else:
            URL = "https://pixabay.com/api/?key=" + API_KEY + "&q=" + urllib.parse.quote(str(q))
            r = requests.get(URL)
            r = r.json()
            sub_dict={}
            if r['totalHits'] > 0:
                counter = 0
                for hit in r['hits']:
                    sub_dict[len(sub_dict)]=[hit["webformatURL"],hit["tags"]]
                    counter += 1
                    if counter == 5:
                        break
                sub_dict
            return Response(sub_dict)
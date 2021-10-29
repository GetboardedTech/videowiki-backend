import json
import requests
from rest_framework import status
from rest_framework.response import Response
def audioList(keywords):
	url = "https://deezerdevs-deezer.p.rapidapi.com/search"
	headers = {
		'x-rapidapi-key': "66c38b790bmshbde7a19d739e396p17abcejsnfd5bf8c5d5aa",
		'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com"
	}
	audio_list={}
	for keys,keyword_list in keywords.items():
		for keyword in keyword_list:
			querystring = {"q": keyword}
			response = requests.request("GET", url, headers=headers, params=querystring)
			res_data=json.loads(response.text)
			counter=0
			for aud_data in res_data["data"]:
				audio_list[len(audio_list)]={"url": aud_data["preview"],"title":aud_data["title"]}
				counter+=1
				if counter==2:
					break
	return Response(audio_list,status.HTTP_200_OK)
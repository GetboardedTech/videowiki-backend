
# Create your views here.

from rake_nltk import Rake
from django.http import JsonResponse
from rest_framework.views import APIView
from googletrans import Translator


class KeywordExtraction(APIView):

	def post(self, request):
		if request.method == 'POST':
			c=0
			d=0
			response_dict={}
			r_d2 = {}
			#print(request.data)
			sentences = request.data['sentences']
			srcLang = request.data['srcLang']
			#print(sentences)
			translator = Translator()
			for k,v in sentences.items():
				#print(k,v)
				r = Rake(max_length=2)
				transObj = translator.translate(v, src=srcLang, dest='en')
				#srcLang = transObj.src
				text = transObj.text
				r.extract_keywords_from_text(text)
				keywords = r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.
				#print(keywords)
				for k2 in keywords[:4]:
					r_d2[d] = str(k2)
					d+=1
				#print(r_d2)
				response_dict[c] = r_d2
				c+=1
				d=0
				r_d2={}
			#print(response_dict)
			return JsonResponse(response_dict)


from rake_nltk import Rake
from gensim.summarization import keywords,mz_keywords
from django.http import JsonResponse
from rest_framework.views import APIView
from polyglot.text import Text
from translate import Translator
limitWarning='MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN  09 HOURS 02 MINUTES 29 SECONDSVISIT HTTPS://MYMEMORY.TRANSLATED.NET/DOC/USAGELIMITS.PHP TO TRANSLATE MORE'
class KeywordExtraction(APIView):
	def post(self, request):
		if request.method == 'POST':
			origin={}
			text = request.data['text']
			srcLang = request.data['srcLang']
			if srcLang!="en":
				e_translator = Translator(to_lang="en",from_lang=srcLang)
				eng_text=str(e_translator.translate(text))
				if eng_text.startswith("MYMEMORY WARNING:"):
					for i in Text(text).sentences:
						origin[len(origin)]=[]
					return JsonResponse(origin)
			else:
				eng_text=text
			for sentence in Text(eng_text).sentences:
				r = Rake(max_length=2)
				r_d2 = []
				r.extract_keywords_from_text(str(sentence))
				key_words = r.get_ranked_phrases()
				if(len(key_words)==0):
					key_words=keywords(str(sentence),words=2,split=True)
				for k2 in key_words[:4]:
					r_d2.append(str(k2))
				origin[len(origin)] = r_d2
			return JsonResponse(origin)

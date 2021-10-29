from .apps import SummarizationConfig

from django.http import JsonResponse
from rest_framework.views import APIView
from translate import Translator
class Summarization(APIView):

	def post(self, request):
		if request.method == 'POST':
			text = request.data['text']
			srcLang=request.data["srcLang"]
			if srcLang!="en":
				text=str(Translator(to_lang="en",from_lang=srcLang).translate(text))
			sc = SummarizationConfig
			parser = sc.parser(text)
			summarizer = sc.summarizer()

			SENTENCES_COUNT = 5

			sent_dict = {}
			c=0

			sentences=''.join([str(sent) for sent in summarizer(parser.document, SENTENCES_COUNT)])
			if srcLang!="en":
				sentences=str(Translator(to_lang=srcLang,from_lang="en").translate(sentences))
			return JsonResponse({'summary':sentences})

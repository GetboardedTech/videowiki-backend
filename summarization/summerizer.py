from gensim.summarization.summarizer import summarize
from django.http import JsonResponse
from rest_framework.views import APIView
from translate import Translator
from polyglot.text import Text
class Summarization(APIView):
    def post(self,request):
        text = request.data['text']
        if len(Text(text).sentences)==1:
            return JsonResponse({'summary':text})
        srcLang=request.data["srcLang"]
        if srcLang!='en':
            text=str(Translator(to_lang="en",from_lang=srcLang).translate(text))
        summary_en=None
        if(len(text.split(" "))<200):
            summary_en=summarize(text,word_count=10)
        else:
            summary_en=summarize(text,word_count=30)
        if srcLang!='en':
            summary=str(Translator(to_lang=srcLang,from_lang="en").translate(summary_en))
            return JsonResponse({'summary':summary})
        else:
            return JsonResponse({'summary':summary_en})

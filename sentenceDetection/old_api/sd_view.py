from django.http import JsonResponse
from rest_framework.views import APIView
from polyglot.text import Text
class SentenceDetectionAPI(APIView):

	sentence_connector = ['further', 'furthermore', 'moreover', 'in addition', 'additionally', 'then', 'also', 'too', 'besides', 'again', 'equally important', 'first, second', 'finally, last',
						  'similarly', 'comparable', 'in the same way', 'likewise', 'as with', 'equally', 'however', 'nevertheless', 'on the other hand', 'on the contrary', 'even so', 'notwithstanding',
						  'alternatively', 'at the same time', 'though', 'otherwise', 'instead', 'nonetheless', 'conversely', 'meanwhile', 'presently', 'at last', 'finally', 'immediately', 'thereafter',
						  'at that time', 'subsequently', 'eventually', 'currently', 'in the meantime', 'in the past', 'hence', 'therefore', 'accordingly', 'consequently', 'thus', 'thereupon', 'as a result',
						  'in consequence', 'so', 'then', 'in short', 'on the whole', 'in other words', 'to be sure', 'clearly', 'anyway', 'in sum', 'after all', 'in general', 'it seems', 'in brief',
						  'for example', 'for instance', 'that is', 'such as', 'as revealed by', 'illustrated by', 'specifically', 'in particular', 'for one thing', 'this can be seen', 'in',
						  'an instance of', 'this', 'there', 'here', 'beyond', 'nearby', 'next to', 'at that point', 'opposite to', 'adjacent to', 'on the other side', 'in the front', 'in the back', 'but']

	def post(self, request):
		if request.method=="POST":
			response_dict = {}
			sentences_short={}
			sentences={}
			text = Text(request.data['text'])
			for sentence in list(text.sentences):
				sentences[len(sentences)] = str(sentence)
			if request.data["break_type"] == "short_sentences":
				short_sen = ""
				for k, v in sentences.items():
					# print(v)
					words = v.split(" ");
					for w in words:
						# print(w)
						if w in self.sentence_connector:
							short_sen = short_sen + " "
							sentences_short[len(sentences_short)] = short_sen[0:-1]
							short_sen = w + " "
						else:
							short_sen = short_sen + w + " "
					sentences_short[len(sentences_short)] = short_sen[0:-1]
					short_sen = ""
				response_dict["sentences"]=sentences_short
			else:
				response_dict["sentences"]=sentences
			return JsonResponse(response_dict)
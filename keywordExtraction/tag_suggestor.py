from rest_framework.views import APIView
from django.http import JsonResponse
import en_core_web_lg
nlp=en_core_web_lg.load()

class TagFinder(APIView):
    def post(self,request):
        response={}
        title=nlp(request.data["title"])
        keywords=request.data["keywords"]
        for keyword in keywords:
            if keyword not in response:
                response[keyword]=float(nlp(keyword).similarity(title))
        #sorting keywords in matching percentage order
        response=[k for k,v in sorted(response.items(),key=lambda item:item[1],reverse=True)]
        return JsonResponse({'tags':response[:5]})

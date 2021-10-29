from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import BuyModel
# Create your views here.

from rest_framework.serializers import ModelSerializer


class BuyVideoSerializer(ModelSerializer):
    class Meta:
        model = BuyModel
        fields = '__all__'


class BuyVideoView(APIView):

    def get(self, request):
        try:
            video_id = request.GET.get('video_id')
            videos = {
                'status':True,
                'data': BuyVideoSerializer(BuyModel.objects.get(video_id=video_id)).data
            }
            return JsonResponse(videos)
        except ObjectDoesNotExist:
            return JsonResponse({'data':"video doesn't exist","status":False})

    def post(self,request):
        if request.method == 'POST':
            data = {
                'exchange_key':request.data['exchange_key'],
                'dod':request.data['dod'],
                'video_id':request.data['video_id'],
                'dataToken':request.data['dataToken'],
                'paid':request.data['paid']
            }
            if BuyModel.objects.filter(video_id=data['video_id']).count() == 0:
                BuyModel.objects.create(**data)
            else:
                BuyModel.objects.filter(video_id=data['video_id']).update(**data)
            return JsonResponse(data)

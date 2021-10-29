from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from videos.models import Video
from .workingAPI import publish_api,update_publish_api,get_video_details
from .workingAPI.serializer import VideoSerializer
from transaction.models import BuyModel

class VideoViewSet(ModelViewSet):
    # countryUpdate()
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'user')
    # pagination_class = PageNumberPagination
    #
    # def filter_queryset(self, queryset):
    #     gte = self.request.GET.get('match_start_date')
    #     lte = self.request.GET.get('match_end_date')
    #     if gte and lte:
    #         return Match.objects.filter(start_date__gte=gte).filter(start_date__lte=lte).order_by('start_date')
    #     return super().filter_queryset(queryset)



class HomeVidoes(APIView):

    def get(self, request):
        if request.method == 'GET':
            data = []
            for video in Video.objects.filter(is_save_later=False):
                trans = BuyModel.objects.filter(video=video)
                data.append({
                    'id':video.id,
                    'title':video.title,
                    'description':video.description,
                    'thumbnail':str(video.thumbnail.url),
                    'video':str(video.video.url),
                    'script':video.script,
                    'user__first_name':video.user.first_name,
                    'user__last_name':video.user.last_name,
                    'rating':video.rating,
                    'publish_time':video.publish_time,
                    'topic':video.topic,
                    'duration':video.duration,
                    'paid': trans[0].paid if trans.count()!=0 else False
                })
            return JsonResponse({"data":data},safe=False)


class UserVidoes(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.method == 'GET':
            vidoes = {
                'data': list(Video.objects.filter(user=request.user).values(
                    'id', 'title', 'description', 'thumbnail', 'video',
                    'script', 'user__first_name', 'user__last_name', 'rating',
                    'publish_time', 'topic','duration','is_save_later'
                )),
            }
            return JsonResponse(vidoes)

class PublishVideo(APIView):
    def post(self,request):
        if bool(request.data["id"]==None) & (bool(request.data["published_id"]==None)|bool(request.data["is_save_later"])):
            return publish_api.publish(request)
        else:
            return update_publish_api.modified_video_publish(request)

class GetSavedVideo(APIView):
    def get(self,request):
        id=request.GET.get("id")
        return get_video_details.get_video(id)
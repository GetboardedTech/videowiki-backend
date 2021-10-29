from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MusicLib
from  .serializer import MusicLibSerializer
from rest_framework.request import Request

class MusicList(APIView):
    def get(self, request):

        music = MusicLib.objects.filter(
            genre=request.GET.get("genre")
        ).order_by("title")
        musicserializer = MusicLibSerializer(music,many=True)
        return Response({'data':musicserializer.data}, status=status.HTTP_200_OK)
    #
    # def post(self, request):
    #     parser_classes = (MultiPartParser, FormParser)
    #     #postserializer = MusicSerializer(data=request.data)
    #     new_music = MusicLib.objects.create(
    #         title = request.data['title'],
    #         genre = request.data['genre'],
    #         upload = request.data['upload']
    #     )
    #     postserializer = MusicSerializer(data=new_music)
    #     if postserializer.is_valid():
    #         postserializer.save()
    #         return Response({'data':postserializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(postserializer.errors, status=status.HTTP_400_BAD_REQUEST)



        







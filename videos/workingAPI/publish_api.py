from coutoEditor.settings import BASE_URL
from videos.models import *
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime,timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def addScenes(data,video):
    vid,aud=None,None
    for i in data:
        proccessed_data = {
            "order":int(i),
            "video_url":data[i]["online_url"],
            "text":data[i]["text"],
            "keywords":",".join(data[i]["keywords"]),
            "font_color":data[i]["font_color"],
            "background_color":data[i]["background_color"],
            "text_position":data[i]["position"]

        }
        if data[i]["uploaded_video"]!=None:
            vid = open(os.path.join(BASE_DIR,data[i]["uploaded_video"].replace(BASE_URL, "")), "rb")
            proccessed_data["video_file"]=File(vid, name=data[i]["uploaded_video"].split('/')[-1])
        if data[i]["audio"]!=None:
            aud = open(os.path.join(BASE_DIR,data[i]["audio"].replace(BASE_URL, "")), "rb")
            proccessed_data["narration"]=File(aud, name=data[i]["audio"].split('/')[-1])
        upload=SceneSerializer(Scenes(video=video),data=proccessed_data)
        if upload.is_valid():
            upload.save()
            if vid!=None:
                vid.close()
            if aud!=None:
                aud.close()
        else:
            return Response(upload.errors,status.HTTP_304_NOT_MODIFIED)
    return Response(status.HTTP_200_OK)

def publish(request):
    img = open(os.path.join(BASE_DIR,request.data["info"]["image"].replace(BASE_URL, "")), "rb")
    vid = open(os.path.join(BASE_DIR,request.data["video"].replace(BASE_URL, "")), "rb")
    data = {'title': request.data["info"]["title"],
            'description': request.data["info"]["description"],
            'thumbnail': File(img, name=request.data["info"]["image"].split('/')[-1]),
            'script': request.data["info"]["script"],
            'video': File(vid, name=request.data["video"].split('/')[-1]),
            'publish_time': datetime.utcnow(),
            'language':request.data["info"]["language"],
            'is_save_later':bool(request.data["is_save_later"]),
            'duration':datetime.strptime(str(timedelta(seconds=int(request.data["info"]["duration"]))),"%H:%M:%S").time()
            }
    if request.data["bgm"] == None:
        data["background_music_file"] = None
        data["background_music_url"] = None
    elif request.data["bgm"].startswith(BASE_URL):
        data["background_music_file"] = File(
            open(os.path.join(BASE_DIR, request.data["bgm"].replace(BASE_URL, "")), "rb"),
            name=request.data["bgm"].split('/')[-1])
        data["background_music_url"] = None
    else:
        data["background_music_url"] = request.data["bgm"]
        data["background_music_file"] = None
    try:
        user = User.objects.get(username=request.data["info"]["user"])
    except:
        return JsonResponse({'error': 'UserDoesNotExist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    upload = VideoSerializer(Video(user=user), data=data)
    if upload.is_valid():
        upload.save()
        img.close()
        vid.close()
        video=Video.objects.get(id=upload.data["id"])
        for tag in request.data["tags"]:
            t=Tags.objects.get_or_create(tag=tag)
            t[0].videos.add(video)
        img.close()
        vid.close()
        resp=addScenes(request.data["scenes"],video)
        if resp.status_code==200 :
            return Response({"id":upload.data["id"]},status=status.HTTP_201_CREATED)
        else:
            video.delete()
            return Response(resp.data,status=status.HTTP_400_BAD_REQUEST)
    return Response(upload.errors, status=status.HTTP_400_BAD_REQUEST)
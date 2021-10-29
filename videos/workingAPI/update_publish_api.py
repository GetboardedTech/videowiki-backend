from coutoEditor.settings import BASE_URL
from django.core.files import File
from datetime import datetime,timedelta
from rest_framework import status
import os
from .serializer import *
from rest_framework.response import Response
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def modified_video_scenes(data,video):
    vid,aud=None,None
    for i in data:
        proccessed_data = {
            "order": int(i),
            "video_url": data[i]["online_url"],
            "text": data[i]["text"],
            "keywords": ",".join(data[i]["keywords"]),
            "font_color": data[i]["font_color"],
            "background_color": data[i]["background_color"],
            "text_position": data[i]["position"]

        }
        if data[i]["uploaded_video"] != None:
            vid = open(os.path.join(BASE_DIR,data[i]["uploaded_video"].replace(BASE_URL, "")), "rb")
            proccessed_data["video_file"] = File(vid, name=data[i]["uploaded_video"].split('/')[-1])
        else:
            proccessed_data["video_file"]=None
        if data[i]["audio"] != None:
            aud = open(os.path.join(BASE_DIR,data[i]["audio"].replace(BASE_URL, "")), "rb")
            proccessed_data["narration"] = File(aud, name=data[i]["audio"].split('/')[-1])
        else:
            proccessed_data["narration"]=None
        scene=Scenes.objects.get_or_create(order=int(i),video=video)[0]
        sceneSerialiser=SceneSerializer(scene,data=proccessed_data,partial=True)
        if sceneSerialiser.is_valid():
            sceneSerialiser.save()
        else:
            return Response(sceneSerialiser.errors,status.HTTP_304_NOT_MODIFIED)
        if vid != None:
            vid.close()
        if aud != None:
            aud.close()
    all_scenes=Scenes.objects.filter(video=video)
    for scene in all_scenes:
        if str(scene.order) not in data.keys():
            scene.delete()
    return Response(status.HTTP_200_OK)

def modified_video_publish(request):
    try:
        if not bool(request.data["is_save_later"]):
            video=Video.objects.get(id=request.data["published_id"])
        else:
            video = Video.objects.get(id=request.data["id"])
    except:
        video=Video.objects.get(id=request.data["id"])
    img = open(os.path.join(BASE_DIR,request.data["info"]["image"].replace(BASE_URL, "")), "rb")
    vid = open(os.path.join(BASE_DIR,request.data["video"].replace(BASE_URL, "")), "rb")
    data = {'title': request.data["info"]["title"],
            'description': request.data["info"]["description"],
            'thumbnail': File(img, name=request.data["info"]["image"].split('/')[-1]),
            'script': request.data["info"]["script"],
            'video': File(vid, name=request.data["video"].split('/')[-1]),
            'publish_time': datetime.utcnow(),
            'language': request.data["info"]["language"],
            'is_save_later': bool(request.data["is_save_later"]),
            'duration': datetime.strptime(str(timedelta(seconds=int(request.data["info"]["duration"]))),
                                          "%H:%M:%S").time()
            }
    if request.data["bgm"]==None:
        data["background_music_file"] = None
        data["background_music_url"] = None
    elif request.data["bgm"].startswith(BASE_URL):
        data["background_music_file"] = File(open(os.path.join(BASE_DIR,request.data["bgm"].replace(BASE_URL, "")), "rb"), name=request.data["bgm"].split('/')[-1])
        data["background_music_url"] = None
    else:
        data["background_music_url"] = request.data["bgm"]
        data["background_music_file"]=None
    uploadVideo=VideoSerializer(video,data=data,partial=True)
    #response from add scene
    Scene_response=modified_video_scenes(request.data["scenes"], video)
    if Scene_response.status_code!=200:
        return Response(Scene_response.data, status=status.HTTP_304_NOT_MODIFIED)
    if uploadVideo.is_valid():
        uploadVideo.save()
        for tags in Tags.objects.filter(videos=video):
            tags.videos.remove(video)
        for tag in request.data["tags"]:
            t = Tags.objects.get_or_create(tag=tag)
            t[0].videos.add(video)
        if (~bool(request.data["is_save_later"])&bool(request.data["published_id"]!=None)):
            if (bool(request.data["id"]!=None) & bool(request.data["id"]!=(request.data["published_id"]))) :
                video = Video.objects.get(id=request.data["id"])
                video.delete()
            id=request.data["published_id"]
        else:
            id=request.data["id"]
        return Response({"id":id},status=status.HTTP_201_CREATED)
    else:
        return Response({"error":uploadVideo.errors},status=status.HTTP_304_NOT_MODIFIED)



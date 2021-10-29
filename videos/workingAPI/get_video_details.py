from videos.models import *
from rest_framework.response import Response
from rest_framework import status
from coutoEditor.settings import BASE_URL
import os

def get_video(id):
    try:
        video=Video.objects.get(id=int(id))
        data={
            "info": {
                "title": video.title,
                "description": video.description,
                "image":os.path.join(BASE_URL,video.thumbnail.url[1:]),
                "script": video.script,
                "user": video.user.username,
                "duration": video.duration,
                "language": video.language
                },
            "id": id,
            "video": os.path.join(BASE_URL,video.video.url[1:]),
            "is_save_later": video.is_save_later,
            "published_id":video.publised_video_id,
            "scenes":{}
            }
        if bool(video.background_music_url==None) & bool(video.background_music_file.name==None):
            data["bgm"]=None
        elif video.background_music_url==None:
            data["bgm"]=os.path.join(BASE_URL,video.background_music_file.url[1:])
        else:
            data["bgm"]=video.background_music_url
        all_scenes=Scenes.objects.filter(video=video)
        for scene in all_scenes:
            data["scenes"][str(scene.order)]={
                "text": scene.text,
                "keywords": scene.keywords.split(","),
                "online_url": scene.video_url,
                "audio":None,
                "uploaded_video": None,
                "position": scene.text_position,
                "font_color": scene.font_color,
                "background_color":scene.background_color
            }
            if scene.narration.name != "":
                data["scenes"][str(scene.order)]["audio"]= os.path.join(BASE_URL, scene.narration.url[1:])
            if scene.video_file.name != "":
                data["scenes"][str(scene.order)]["uploaded_video"]= os.path.join(BASE_URL, scene.uploaded_video.url[1:]),
        data["tags"]=[]
        for tags in Tags.objects.filter(videos=video):
            data["tags"].append(tags.tag)
        return Response(data,status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"Error":"Video doesn't exist"},status.HTTP_404_NOT_FOUND)
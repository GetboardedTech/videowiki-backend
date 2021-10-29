# Create your views here.
from image.motion import *
from videos.models import TemporaryFiles
from django.core.files import File
from django.http import JsonResponse
import uuid
import math
from datetime import datetime
import os
from coutoEditor.settings import BASE_URL


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clip_chunks(txt, txt_position, script_color,bg_color,sceneDur,w,h):
    txt_list = txt.split()
    txt_list_chunks = [txt_list[x:x + 5] for x in range(0, len(txt_list), 5)]
    cvc = []
    c = 0
    for tl in txt_list_chunks:
        tl_join = " ".join(tl)
        txt_clip = TextClip(" " + tl_join + " ", color=script_color, fontsize=20,
                            font='Georgia-Bold')
        txt_clip = txt_clip.on_color(size=(10+txt_clip.w, txt_clip.h+10),color=(0,0,0),col_opacity=0.5)
        txt_clip = txt_clip.set_position(('center', txt_position), relative=True)
        # txt_clip = txt_clip.set_pos(lambda t: (max(w / 30, int(w - 0.5 * w * t)), max(5 * h / 6, int(100 * t))))
        txt_clip = txt_clip.set_duration(sceneDur)
        cvc.append(txt_clip.set_start(c))
        txt_clip.close()
        c += sceneDur
    return cvc


def merger(request):
    file_name = str(uuid.uuid4())
    targetname = str(uuid.uuid4())
    txt = request.data['sceneScript']
    script_color = request.data['sceneScriptColor']
    bg_color = request.data['sceneBackgroundColor']
    if (script_color == bg_color):
        bg_color = '#FFFFFF'
    # duration of each clip is of 3s
    #scene_len = int(math.ceil((len(txt.split()) * 3) / 5))
    nclips = math.ceil(len(txt.split()) / 5)
    video = request.data['url']
    """if request.data["type"]!=None:
        resp=zooming(video,request.data["type"],nclips*3)
        video=resp.data["url"]"""
    if video.startswith(BASE_URL):
        video=video.replace(BASE_URL,"")
        video_sub_clip = VideoFileClip(os.path.join(BASE_DIR, video)).resize(width=720,height=720)
    else:
        video_sub_clip = VideoFileClip(video)
    sceneDur=video_sub_clip.duration/nclips

    txt_position = 'center'
    if request.data['sceneScriptPosition'] == 1:
        txt_position = 0.1
    elif request.data['sceneScriptPosition'] == 2:
        txt_position = 'center'
    elif request.data['sceneScriptPosition'] == 3:
        txt_position = 0.8

    cvc = clip_chunks(txt, txt_position, script_color, bg_color,sceneDur,video_sub_clip.w,video_sub_clip.h)
    cvc.insert(0, video_sub_clip)
    video_with_title_overlay = CompositeVideoClip(cvc)
    video_with_title_overlay.write_videofile(os.path.join(BASE_DIR, "media/edit-script/" + file_name + ".mp4"))
    generated_video=open(os.path.join(BASE_DIR,"media/edit-script/" + file_name + ".mp4"),"rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=file_name + ".mp4"),
                                               created_at=datetime.utcnow())
    generated_video.close()
    if os.path.exists(os.path.join(BASE_DIR, "media/trimmed-videos/" + targetname + ".mp4")):
        os.remove(os.path.join(BASE_DIR, "media/trimmed-videos/" + targetname + ".mp4"))
    os.remove(os.path.join(BASE_DIR,"media/edit-script/" + file_name + ".mp4"))
    video_sub_clip.close()
    video_with_title_overlay.close()
    res_dict = {
        "video_url": os.path.join(BASE_URL,video_file.temp_file.url[1:])
    }
    return JsonResponse(res_dict)

from moviepy.editor import *
from videos.models import TemporaryFiles
from django.http import JsonResponse
from moviepy.video import fx
from datetime import datetime
from django.core.files import File
import os
import uuid

from coutoEditor.settings import BASE_URL
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def merger(data):
    file_name = str(uuid.uuid4())
    if not os.path.exists("media/audio-video-merged/"):
        os.mkdir("media/audio-video-merged/")
    v = data['video']
    if v.startswith(BASE_URL):
        v = os.path.join(BASE_DIR,v.replace(BASE_URL, ""))
    video = VideoFileClip(v)
    video_time = video.duration
    file = data['audio']
    if str(file).startswith("https://") and not str(file).startswith(BASE_URL):
        file_path=str(file)
        audio = AudioFileClip(file_path).set_duration(video_time)
    else:
        if str(file).startswith(BASE_URL):
            file_path=os.path.join(BASE_DIR,str(file).replace(BASE_URL,""))
        else:
            audio_file = TemporaryFiles.objects.create(temp_file=file, created_at=datetime.utcnow())
            file_path = os.path.join(BASE_DIR,audio_file.temp_file.url[1:])
        audio = AudioFileClip(file_path)
    audio_time = audio.duration
    if (video_time >= audio_time):
        video = video.set_duration(audio_time)
    else:
        video = fx.all.loop(video, duration=audio_time)
    video_with_audio = CompositeVideoClip([video.set_audio(audio)])
    video_with_audio.write_videofile(os.path.join(BASE_DIR, "media/audio-video-merged/" + file_name + ".mp4"),
                                     preset="ultrafast")
    video_with_audio.close()
    generated_video=open(os.path.join(BASE_DIR,"media/audio-video-merged/" + file_name + ".mp4"),"rb")
    video_file=TemporaryFiles.objects.create(temp_file=File(generated_video,name=file_name + ".mp4"),created_at=datetime.utcnow())
    generated_video.close()
    os.remove(os.path.join(BASE_DIR,"media/audio-video-merged/" + file_name + ".mp4"))
    audio.close()
    video.close()
    if not file_path.startswith("https://"):
        file_path=os.path.join(BASE_URL,file_path.replace(BASE_DIR,"")[1:])
    res_dict = {
        "video_url": os.path.join(BASE_URL,video_file.temp_file.url[1:]),
        "audio_url":file_path
    }
    return JsonResponse(res_dict)
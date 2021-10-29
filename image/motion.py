from rest_framework.response import Response
from moviepy.editor import *
from coutoEditor.settings import BASE_DIR
from uuid import uuid4
import requests
from moviepy.video import fx
from coutoEditor.settings import BASE_URL
from django.core.files import File
from videos.models import TemporaryFiles
from datetime import datetime

def motion(image_url,type,length=3):
    filename=str(uuid4())
    download_path=os.path.join(BASE_DIR,"media/images/")
    if not os.path.exists(os.path.join(BASE_DIR,"media/images/")):
        os.mkdir(os.path.join(BASE_DIR,"media/images/"))
    r=requests.get(image_url)
    open(download_path+filename+"."+image_url.split(".")[-1],"wb").write(r.content)
    screen_size=(1280,720)

    def zoom_in(t):
        if t < duration:
            return 1 + 0.05 * t  # Zoom-in.
    def zoom_out(t):
        if t == 0:
            return 1 + 0.5 # Zoom-in. 1.2
        else:
            return 1 + 0.05 * (duration - t) # Zoom-out. 1.08
    def both(t):
        if t <= 5:
            return 1 + 0.05 * t# Zoom-in. 1.2
        else:
            return 1 + 0.05 * (duration - t) # Zoom-out. 1.08

    if type=="in":
        resize_func=zoom_in
        duration = 3
    elif type=="out":
        resize_func=zoom_out
        duration = 3
    elif type == "None":
        resize_func = None
        duration = 3
    else:
        resize_func=both
        duration = 3

    if resize_func:
        clip_img = (
            ImageClip(download_path+filename+"."+image_url.split(".")[-1])
                .resize(screen_size)
                .resize(resize_func)
                .set_position(('center', 'center'))
                .set_duration(duration)
                .set_fps(25)
        )
    else:
        clip_img = (
            ImageClip(download_path + filename + "." + image_url.split(".")[-1])
                .resize(screen_size)
                .set_position(('center', 'center'))
                .set_duration(duration)
                .set_fps(25)
        )
    clip = CompositeVideoClip([clip_img], size=(screen_size))
    video=fx.all.loop(clip, duration=length)
    video.write_videofile(os.path.join(BASE_DIR,"media/images/"+filename+".mp4"),preset="ultrafast")


    generated_video = open(os.path.join(BASE_DIR,"media/images/"+filename+".mp4"), "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                               created_at=datetime.utcnow())
    generated_video.close()
    clip.close()
    video.close()

    if os.path.exists(download_path+filename+"."+image_url.split(".")[-1]):
        os.remove(download_path+filename+"."+image_url.split(".")[-1])
    if os.path.exists(os.path.join(BASE_DIR,"media/images/"+filename+".mp4")):
        os.remove(os.path.join(BASE_DIR,"media/images/"+filename+".mp4"))

    return Response({"url":os.path.join(BASE_URL, video_file.temp_file.url[1:])})

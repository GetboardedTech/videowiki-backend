from PIL import Image
from moviepy.editor import *
from datetime import datetime
from django.core.files import File
from videos.models import TemporaryFiles
from coutoEditor.settings import BASE_URL
import uuid
import os
import math
from pydub import AudioSegment
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def background_music_adder(bgm_url,final_video_url):
    filename=str(uuid.uuid4())
    if bgm_url.startswith(BASE_URL):
        bgm_url=os.path.join(BASE_DIR,bgm_url.replace(BASE_URL,""))
    # Adding background music
    video = VideoFileClip(final_video_url)
    if video.audio!=None:
        video.audio.write_audiofile(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp3"))
        bgm = AudioFileClip(bgm_url)
        bgm.write_audiofile(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_bgm.mp3"))
        bgm.close()
        video.close()
        sound1 = AudioSegment.from_file(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp3"))
        sound2 = AudioSegment.from_file(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_bgm.mp3"))
        combined = sound1.overlay(sound2, loop=True)
        combined.export(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_final.mp3"), format='mp3')

        final_audio = AudioFileClip(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_final.mp3"))
        video = VideoFileClip(final_video_url)
        video_bgm = video.set_audio(final_audio)
    else:
        video = VideoFileClip(final_video_url)
        bgm = AudioFileClip(bgm_url)
        n_loops=int(math.ceil(video.duration/bgm.duration))
        bgm=bgm.audio_loop(n_loops)
        bgm=bgm.set_duration(video.duration)
        video_bgm = video.set_audio(bgm)
    video_bgm.write_videofile(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp4"))

    if os.path.exists(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp3")):
        os.remove(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp3"))

    if os.path.exists(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_bgm.mp3")):
        os.remove(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_bgm.mp3"))

    if os.path.exists(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_final.mp3")):
        final_audio.close()
        os.remove(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + "_final.mp3"))
    if ~bool(final_video_url.startswith("/home/hsubramani42/Documents/videowiki-backend/media/temp")) & bool(os.path.exists(final_video_url)):
        os.remove(final_video_url)
    video.close()
    video_bgm.close()
    return os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp4")


def video_concatenation(videos,resolution,bgm_url):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    video_list=[]
    res_dict={}
    filename=str(uuid.uuid4())

    for video in videos:
        if video.startswith(BASE_URL):
            video = os.path.join(BASE_DIR,video.replace(BASE_URL,""))
        video_list.append(VideoFileClip(video).resize(height=resolution, width=resolution))

    for i , video in enumerate(video_list):
        duration = min(video.duration,8)
        video_list[i] = video.set_duration(duration)

    final_video = concatenate_videoclips(video_list)
    concatenate_file_url=os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp4")
    final_video.write_videofile(concatenate_file_url)
    if bgm_url!=None:
        concatenate_file_url=background_music_adder(bgm_url, concatenate_file_url)
    thumbnail = final_video.get_frame(1)
    img = Image.fromarray(thumbnail)
    img = img.resize((1280, 720), Image.ANTIALIAS)
    img.save(os.path.join(BASE_DIR,"media/concatenated-videos/" + str(filename) + ".png"))
    for video in video_list: video.close()
    final_video.close()
    generated_img = open(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".png"), "rb")
    generated_video = open(concatenate_file_url, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                               created_at=datetime.utcnow())
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                               created_at=datetime.utcnow())
    generated_img.close()
    generated_video.close()
    if os.path.exists(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png")):
        os.remove(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png"))
    if os.path.exists(concatenate_file_url):
        os.remove(concatenate_file_url)
    res_dict["image_url"]=os.path.join(BASE_URL,image_file.temp_file.url[1:])
    res_dict["video_url"] = os.path.join(BASE_URL,video_file.temp_file.url[1:] )
    return res_dict

def single_video_concat(request,resolution,bgm_url):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    filename = str(uuid.uuid4())
    newFilename = str(uuid.uuid4())
    online_video=True
    video_url = request.data["videos"][0]
    if video_url.startswith(BASE_URL):
        video_url = os.path.join(BASE_DIR,video_url.replace(BASE_URL, ""))
        online_video = False
    video = VideoFileClip(video_url).resize(height=resolution, width=resolution)
    thumbnail = video.get_frame(1)
    img = Image.fromarray(thumbnail)
    img = img.resize((1280, 720), Image.ANTIALIAS)
    img.save(os.path.join(BASE_DIR,"media/concatenated-videos/" + str(filename) + ".png"))
    generated_img=open(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png"),"rb")
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                               created_at=datetime.utcnow())
    generated_img.close()
    del img
    os.remove(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png"))
    if online_video:
        video.write_videofile(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".mp4"),preset="ultrafast")
        generated_video = open(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".mp4"), "rb")
        video_file=TemporaryFiles.objects.create(temp_file=File(generated_video,name=filename + ".mp4"),created_at=datetime.utcnow())
        video_url=video_file.temp_file.url[1:]
        generated_video.close()
        os.remove(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".mp4"))
    video.close()
    if bgm_url!=None:
        print(video_url)
        newFilename=background_music_adder(bgm_url,os.path.join(BASE_DIR,video_url))
        generated_video = open(newFilename, "rb")
        video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                   created_at=datetime.utcnow())
        video_url = video_file.temp_file.url[1:]
        generated_video.close()
        os.remove(newFilename)
    response = {'video_url': BASE_URL + video_url,
               'image_url': BASE_URL + image_file.temp_file.url[1:]}
    return JsonResponse({'status': True, 'data': response})

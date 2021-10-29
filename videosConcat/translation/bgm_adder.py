from PIL import Image
from moviepy.editor import *
from datetime import datetime
from django.core.files import File
from videos.models import TemporaryFiles
from coutoEditor.settings import BASE_URL, BASE_DIR
import uuid
import os
import math
from pydub import AudioSegment
from django.http import JsonResponse

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def background_music_adder(bgm_url, final_video_url):
    filename=str(uuid.uuid4())
    if bgm_url.startswith(BASE_URL):
        bgm_url = os.path.join(BASE_DIR, bgm_url.replace(BASE_URL, ""))
    # Adding background music
    video = VideoFileClip(final_video_url)
    if video.audio!= None:
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
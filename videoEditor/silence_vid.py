import moviepy.editor as mp
import os
from rest_framework import status
import uuid
from videos.models import TemporaryFiles
from datetime import datetime
from django.core.files import File
#import ffmpeg
from django.http import JsonResponse
from moviepy.editor import AudioFileClip, VideoFileClip
from coutoEditor.global_variable import BASE_URL, BASE_DIR


def aud_url(video_url):
    filename = str(uuid.uuid4())
    res_dict = {}
    vid_inp = video_url
    vid_out = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp4")
    aud_out = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp3")
    cmd = "ffmpeg -i " + vid_inp + " -c copy -an " + vid_out
    terminal = "ffmpeg -i " + vid_inp + " -f mp3 -ab 192000 -vn " + aud_out
    os.system(cmd)
    os.system(terminal)
    generated_video = open(vid_out, "rb")
    generated_audio = open(aud_out, "rb")
    generated_video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                         created_at=datetime.utcnow())
    generated_audio_file = TemporaryFiles.objects.create(temp_file=File(generated_audio, name=filename + ".mp3"),
                                                         created_at=datetime.utcnow())
    generated_video.close()
    generated_audio.close()
    if os.path.exists(vid_out):
        os.remove(vid_out)
    if os.path.exists(aud_out):
        os.remove(aud_out)
    res_dict["video_url"] = os.path.join(BASE_URL, generated_video_file.temp_file.url[1:])
    res_dict["audio_url"] = os.path.join(BASE_URL, generated_audio_file.temp_file.url[1:])
    return JsonResponse({"data": res_dict}, status=status.HTTP_200_OK)


# def aud_url(video_url):
#     filename = str(uuid.uuid4())
#     res_dict = {}
#     videoclip = VideoFileClip(video_url)
#     audioclip = AudioFileClip(video_url)
#     vid_url = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp4")
#     audio_url = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp3")
#     audioclip.write_audiofile(audio_url)
#     audioclip.close()
#     videoclip = videoclip.without_audio()
#     videoclip.write_videofile(vid_url)
#     videoclip.close()
#     generated_audio = open(audio_url, "rb")
#     generated_video = open(vid_url, "rb")
#     generated_file = TemporaryFiles.objects.create(temp_file=File(generated_audio, name=filename + ".mp3"), created_at=datetime.utcnow())
#     generated_video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"), created_at=datetime.utcnow())
#     generated_audio.close()
#     generated_video.close()
#     if os.path.exists(audio_url):
#         os.remove(audio_url)
#     if os.path.exists(vid_url):
#          os.remove(vid_url)
#     res_dict["audio_url"] = os.path.join(BASE_URL,generated_file.temp_file.url[1:])
#     res_dict["video_url"] = os.path.join(BASE_URL, generated_video_file.temp_file.url[1:])
#     return JsonResponse({"data": res_dict}, status=status.HTTP_200_OK)



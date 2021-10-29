from PIL import Image
from moviepy.editor import ImageClip, VideoFileClip
from datetime import datetime
from django.core.files import File
from videos.models import TemporaryFiles
from coutoEditor.settings import BASE_URL, BASE_DIR
import uuid
import os
from django.http import JsonResponse
from .translation.translation_funcs import no_motion, slide_in_right, slide_in_left, slide_in_top, slide_in_bottom, fade_in, fade_out
from .translation.bgm_adder import background_music_adder
import requests


def merge(v1, v2, motion):
    videos = [v1, v2]
    if motion == "slide_in_right":
        return slide_in_right(videos)
    elif motion == "no_motion":
        return no_motion(videos)
    elif motion == "slide_in_left":
        return slide_in_left(videos)
    elif motion == "slide_in_top":
        return slide_in_top(videos)
    elif motion == "slide_in_bottom":
        return slide_in_bottom(videos)
    elif motion == "fade_in":
        return fade_in(videos)
    elif motion == "fade_out":
        return fade_out(videos)

    return None


def translated_concatenation(videos, motions, isPreview,bgm_url):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    filename = str(uuid.uuid4())
    res_dict = {}
    video_list = []
    w,h = 1280,720
    if isPreview==1:
        w,h=720,480

    if len(motions) == 0:
        for _ in range(len(videos)-1):
            motions.append('no_motion')

    # image download path
    download_path = os.path.join(BASE_DIR, "media/images/")
    if not os.path.exists(os.path.join(BASE_DIR, "media/images/")):
        os.mkdir(os.path.join(BASE_DIR, "media/images/"))

    for video in videos:
        if video.endswith(".jpg") or video.endswith(".png") or video.endswith(".jpeg"):
            if video.startswith(BASE_URL):
                video = os.path.join(BASE_DIR, video.replace(BASE_URL, ""))
                video_list.append((ImageClip(video))
                                  .set_duration(3)
                                  .set_position(("center", "center"))
                                  .set_fps(25)
                                  .resize( width=w,height=h)
                                  )
            else:
                img_data = requests.get(video)
                open(download_path + filename + "." + video.split(".")[-1], "wb").write(img_data.content)
                video_list.append(ImageClip(download_path + filename + "." + video.split(".")[-1])
                                  .set_duration(3)
                                  .set_position(("center", "center"))
                                  .set_fps(25)
                                  .resize(width=w, height=h)
                                  )

        else:
            if video.startswith(BASE_URL):
                video = os.path.join(BASE_DIR, video.replace(BASE_URL, ""))
                video_list.append(VideoFileClip(video).resize(height=h, width=w))
            else:
                video_list.append(VideoFileClip(video).resize(height=h, width=w))

    v = merge(video_list[0], video_list[1], motions[0])
    j = 1
    for i in range(2, len(video_list)):
        v = merge(v, video_list[i], motions[j])
        j += 1
    combined_video_url=os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".mp4")
    v.write_videofile(combined_video_url)
    if bgm_url!=None:
        combined_video_url=background_music_adder(bgm_url, combined_video_url)
    thumbnail = v.get_frame(1)
    img = Image.fromarray(thumbnail)
    img = img.resize((1280, 720), Image.ANTIALIAS)
    img.save(os.path.join(BASE_DIR, "media/concatenated-videos/" + str(filename) + ".png"))
    for video in video_list: video.close()
    v.close()
    img.close()
    generated_img = open(os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".png"), "rb")
    generated_video = open(combined_video_url, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                               created_at=datetime.utcnow())
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                               created_at=datetime.utcnow())
    generated_img.close()
    generated_video.close()
    if os.path.exists(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png")):
        os.remove(os.path.join(BASE_DIR,"media/concatenated-videos/" + filename + ".png"))
    if os.path.exists(combined_video_url):
        os.remove(combined_video_url)
    res_dict["image_url"]=os.path.join(BASE_URL,image_file.temp_file.url[1:])
    res_dict["video_url"] = os.path.join(BASE_URL,video_file.temp_file.url[1:] )
    return res_dict


def single_video_concat(request,isPreview,bgm_url):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    filename = str(uuid.uuid4())
    newFilename = str(uuid.uuid4())
    online_video=True
    video_url = request.data["videos"][0]

    w, h = 1280, 720
    if isPreview == 1:
        w, h = 720, 480

    if video_url.startswith(BASE_URL):
        video_url = os.path.join(BASE_DIR,video_url.replace(BASE_URL, ""))
        online_video = False
    video = VideoFileClip(video_url).resize( width=w,height=h)
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
        newFilename=background_music_adder(bgm_url,os.path.join(BASE_DIR,video_url))
        generated_video = open(newFilename, "rb")
        video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                   created_at=datetime.utcnow())
        video_url = video_file.temp_file.url[1:]
        generated_video.close()
        os.remove(newFilename)
    response = {'video_url': BASE_URL + video_url.replace(BASE_DIR,""),
               'image_url': BASE_URL + image_file.temp_file.url[1:]}
    return JsonResponse({'status': True, 'data': response})

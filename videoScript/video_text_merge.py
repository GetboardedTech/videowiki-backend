# Create your views here.
from image.motion import *
from videos.models import TemporaryFiles
from django.core.files import File
from django.http import JsonResponse
import uuid
from datetime import datetime
import os
from coutoEditor.settings import BASE_URL
from PIL import ImageColor
from functools import partial

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# return sentence wise split para
def splitparagraph(para, sentence_len):
    sentences = []
    temp = ''
    for x in para.split():
        temp += x + " "
        if len(temp) >= sentence_len:
            sentences.append(temp)
            temp = ''
    if temp != '':
        sentences.append(temp)
    para = ''
    for x in sentences:
        para += x + '\n'
    return para


# return list of sentences
def paraToSentence(para, no_of_char_in_one_sentence):
    sentences = []
    temp = ''
    for x in para.split():
        temp += x + " "
        if len(temp) >= no_of_char_in_one_sentence:
            sentences.append(temp)
            temp = ''

    if temp != '':
        sentences.append(temp)
    return sentences


# return text_clip as formatted paragraph
def FormattedPara(txt, no_of_char_in_one_sentence, script_color, bg_color, w, h, sceneDur, bg_opacity):
    pad_w, pad_h = 25, 15

    final_txt_clips = []
    clip = TextClip(splitparagraph(para=txt, sentence_len=no_of_char_in_one_sentence),
                    font='Montserrat', kerning=3,
                    fontsize=14, color=script_color, align='west'
                    ).set_duration(sceneDur)
    clip = clip.on_color(size=(pad_w + clip.w, clip.h + pad_h), color=(ImageColor.getrgb(bg_color)),
                         col_opacity=bg_opacity,
                         pos='bottom')
    clip = clip.resize(width=w / 3, height=h / 4)
    clip.close()

    return clip


# function to handle text at top
def text_top(para, script_color, bg_color, w, h, sceneDur, bg_opacity, transition_type):
    para_words = len(para.split())

    # if words in para is > 30. then sentences will be long(70 char in a sentence) else short(40 char in a sentence)
    no_of_char_in_one_sentence = 40
    if para_words > 30:
        no_of_char_in_one_sentence = 60
        sentences = paraToSentence(para, no_of_char_in_one_sentence)
    else:
        no_of_char_in_one_sentence = 40
        sentences = paraToSentence(para, no_of_char_in_one_sentence)

    tot_sentences = len(sentences)

    # if sceneDur is less than total sentences(long or short) then clip will be formatted para else transitioned
    # sentences
    if tot_sentences > sceneDur or tot_sentences > 5:
        final_txt_clips = []
        clip = FormattedPara(para, no_of_char_in_one_sentence, script_color, bg_color, w, h, sceneDur,
                             bg_opacity)

        def get_pos(t):
            if transition_type == 'left_to_right':
                return min(w / 30, -int(w - 1.2 * w * t)), 30
            else:
                return max(w / 30, int(w - 1.2 * w * t)), 30

        clip = clip.set_position(partial(get_pos))
        final_txt_clips.append(clip)
        return final_txt_clips

    else:
        for_position = 'top'
        pad_w, pad_h = 25, 15
        pos = []  # 30,80,..

        start_ht = 30
        for each_sent_pos in range(tot_sentences):
            pos.append(start_ht + 50 * each_sent_pos)

        final_txt_clips = []
        i = 0
        for txt in sentences:
            def get_pos(t, i2):
                if transition_type == 'left_to_right':
                    return min(w / 30, -int(w - 1.2 * w * t)), pos[i2]
                else:
                    return max(w / 30, int(w - 1.2 * w * t)), pos[i2]

            txt_clip = TextClip(txt, fontsize=14, font='Montserrat', kerning=2, color=script_color)
            txt_clip = txt_clip.on_color(
                size=(pad_w + txt_clip.w, pad_h + txt_clip.h),
                color=(ImageColor.getrgb(bg_color)),
                col_opacity=bg_opacity,
            )
            txt_clip = txt_clip.set_position(partial(get_pos, i2=i)).set_duration(sceneDur - i)
            txt_clip = txt_clip.resize(width=w / 3.5, height=h / 15)
            final_txt_clips.append(txt_clip.set_start(i))
            i += 1
            txt_clip.close()

        return final_txt_clips


# function to handle text at center
def text_center(para, script_color, bg_color, w, h, sceneDur, bg_opacity, transition_type):
    para_words = len(para.split())
    no_of_char_in_one_sentence = 40
    txt_position = 'center'
    # long sentence
    if para_words >= 40:
        no_of_char_in_one_sentence = 40
        sentences = paraToSentence(para, no_of_char_in_one_sentence)
    else:
        no_of_char_in_one_sentence = 40
        sentences = paraToSentence(para, no_of_char_in_one_sentence)

    tot_sentences = len(sentences)

    if tot_sentences > sceneDur - 1 or tot_sentences > 5:
        final_txt_clips = []
        clip = FormattedPara(para, no_of_char_in_one_sentence, script_color, bg_color, w, h, sceneDur,
                             bg_opacity)

        def get_pos(t):
            if transition_type == 'left_to_right':
                return min(w / 3.5, -int(w - 1.2 * w * t)), txt_position
            else:
                return max(w / 3.5, int(w - 1.2 * w * t)), txt_position

        clip = clip.set_position(partial(get_pos))
        final_txt_clips.append(clip)

    else:
        pad_w, pad_h = 25, 15
        pos = []  # 240,290

        start_ht = 240
        for each_sent_pos in range(tot_sentences):
            pos.append(start_ht + 50 * each_sent_pos)

        final_txt_clips = []
        i = 0
        for txt in sentences:
            def get_pos(t, i2):
                if transition_type == 'left_to_right':
                    return min(w / 3.5, -int(w - 1.2 * w * t)), pos[i2]
                else:
                    return max(w / 3.5, int(w - 1.2 * w * t)), pos[i2]

            txt_clip = TextClip(txt, fontsize=14, font='Montserrat', kerning=2, color=script_color)
            txt_clip = txt_clip.on_color(
                size=(pad_w + txt_clip.w, pad_h + txt_clip.h),
                color=(ImageColor.getrgb(bg_color)),
                col_opacity=bg_opacity,
            )
            txt_clip = txt_clip.set_position(partial(get_pos, i2=i)).set_duration(sceneDur - i)
            txt_clip = txt_clip.resize(width=w / 3.5, height=h / 15)
            final_txt_clips.append(txt_clip.set_start(i))
            i += 1
            txt_clip.close()

    return final_txt_clips


# function to handle text at bottom
def text_bottom(para, script_color, bg_color, w, h, sceneDur, bg_opacity, transition_type):
    para_words = len(para.split())

    no_of_char_in_one_sentence = 40

    # if words in para is > 30. then sentences will be long(70 char in a sentence) else short(40 char in a sentence)
    if para_words > 30:
        no_of_char_in_one_sentence = 60
        sentences = paraToSentence(para, no_of_char_in_one_sentence)
    else:
        no_of_char_in_one_sentence = 40
        sentences = paraToSentence(para, no_of_char_in_one_sentence)

    tot_sentences = len(sentences)

    # if sceneDur is less than total sentences(long or short) then clip will be formatted para else transitioned
    # sentences
    if tot_sentences > sceneDur or tot_sentences > 5:
        final_txt_clips = []
        clip = FormattedPara(para, no_of_char_in_one_sentence, script_color, bg_color, w, h, sceneDur, bg_opacity)

        def get_pos(t):
            if transition_type == 'left_to_right':
                return min(w / 30, -int(w - 1.2 * w * t)), 460
            else:
                return max(w / 30, int(w - 1.2 * w * t)), 460

        clip = clip.set_position(partial(get_pos))
        final_txt_clips.append(clip)

    else:
        pad_w, pad_h = 25, 15
        pos = []  # 600,550
        end_ht = 600
        for each_sent_pos in range(0, tot_sentences):
            pos.append(end_ht - 50 * each_sent_pos)
        pos.reverse()

        final_txt_clips = []
        i = 0
        for txt in sentences:
            def get_pos(t, i2):
                if transition_type == 'left_to_right':
                    return min(w / 30, -int(w - 1.2 * w * t)), pos[i2]
                else:
                    return max(w / 30, int(w - 1.2 * w * t)), pos[i2]

            txt_clip = TextClip(txt, fontsize=14, font='Montserrat', kerning=2, color=script_color)
            txt_clip = txt_clip.on_color(
                size=(pad_w + txt_clip.w, pad_h + txt_clip.h),
                color=(ImageColor.getrgb(bg_color)),
                col_opacity=bg_opacity,
            )
            txt_clip = txt_clip.set_position(partial(get_pos, i2=i)).set_duration(sceneDur - i)
            txt_clip = txt_clip.resize(width=w / 3.5, height=h / 15)
            final_txt_clips.append(txt_clip.set_start(i))
            i += 1
            txt_clip.close()

    return final_txt_clips


def clip_chunks(txt, txt_position, script_color, bg_color, w, h, sceneDur,bg_opacity,transition_type):
    # top
    if txt_position == 1:
        clip = text_top(txt, script_color,
                        bg_color, w, h, sceneDur,bg_opacity,transition_type)

    # center
    elif txt_position == 2:
        clip = text_center(txt, script_color,
                           bg_color, w, h, sceneDur,bg_opacity,transition_type)

    # bottom
    elif txt_position == 3:
        clip = text_bottom(txt, script_color,
                           bg_color, w, h, sceneDur,bg_opacity,transition_type)

    return clip



def merger(request):
    file_name = str(uuid.uuid4())
    targetname = str(uuid.uuid4())
    txt = request.data['sceneScript']
    script_color = request.data['sceneScriptColor']
    bg_color = request.data['sceneBackgroundColor']

    video_url = request.data['url']

    #image download path
    download_path = os.path.join(BASE_DIR, "media/images/")
    if not os.path.exists(os.path.join(BASE_DIR, "media/images/")):
        os.mkdir(os.path.join(BASE_DIR, "media/images/"))

    if video_url.startswith(BASE_URL):
        video_url = video_url.replace(BASE_URL, "")
        if video_url.endswith(".jpg") or video_url.endswith(".png") or video_url.endswith(".jpeg"):
            # r = requests.get(video_url)
            # open(download_path + file_name + "." + video_url.split(".")[-1], "wb").write(r.content)
            video = ImageClip(os.path.join(BASE_DIR, video_url)).set_duration(3).set_fps(25)
        else:
            video = VideoFileClip(os.path.join(BASE_DIR, video_url))
        video_sub_clip = video.resize(
            width=1280, height=720)
    else:
        if video_url.endswith(".jpg") or video_url.endswith(".png") or video_url.endswith(".jpeg"):
            r = requests.get(video_url)
            open(download_path + file_name + "." + video_url.split(".")[-1], "wb").write(r.content)
            video = ImageClip(download_path+file_name+"."+video_url.split(".")[-1]).set_duration(3).set_fps(25)
        else:
            video = VideoFileClip(video_url)
        video_sub_clip = video.resize(
            width=1280, height=720)     #todo variable height and width

    sceneDur = video_sub_clip.duration
    w = video_sub_clip.w
    h = video_sub_clip.h
    txt_position = request.data['sceneScriptPosition']

    try:
        bg_opacity = request.data['bg_opacity']
    except KeyError :
        bg_opacity = 0.8

    try:
        transition_type = request.data['transition_type']
    except KeyError :
        transition_type = "left_to_right"

    txt_clips = clip_chunks(
        txt=txt,
        txt_position=txt_position,
        script_color=script_color,
        bg_color=bg_color,
        w=w, h=h,
        sceneDur=sceneDur,
        bg_opacity=bg_opacity,
        transition_type=transition_type
    )

    video_with_title_overlay = CompositeVideoClip(
        [video_sub_clip] + txt_clips)

    video_with_title_overlay.write_videofile(os.path.join(
        BASE_DIR, "media/edit-script/" + file_name + ".mp4"))
    generated_video = open(os.path.join(
        BASE_DIR, "media/edit-script/" + file_name + ".mp4"), "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=file_name + ".mp4"),
                                               created_at=datetime.utcnow())
    for clip in txt_clips: clip.close()
    video_sub_clip.close()
    video_with_title_overlay.close()
    generated_video.close()

    if os.path.exists(os.path.join(BASE_DIR, "media/trimmed-videos/" + targetname + ".mp4")):
        os.remove(os.path.join(
            BASE_DIR, "media/trimmed-videos/" + targetname + ".mp4"))
    os.remove(os.path.join(BASE_DIR, "media/edit-script/" + file_name + ".mp4"))


    res_dict = {
        "video_url": os.path.join(BASE_URL, video_file.temp_file.url[1:])
    }
    return JsonResponse(res_dict)

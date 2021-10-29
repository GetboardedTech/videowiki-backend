import speech_recognition as sr
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub.utils import mediainfo
import os
from shutil import rmtree
from moviepy.editor import AudioFileClip
from pydub import AudioSegment


def video_to_txt(video_file):
    # try:
    #     rmtree('/home/akdas/clip_chunks')
    # except:
    #     pass

    # os.mkdir('/home/akdas/clip_chunks')

    # num_seconds_video= int(round(float(mediainfo(video_file)['duration'])))

    def match_target_amplitude(sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    # try:
    #     video_file = video_file.split('/')[-1]
    # except:
    #     pass

    audio_file = video_file.split('.')[0] + '_audio.wav'
    audioclip = AudioFileClip(video_file)
    audioclip.write_audiofile(audio_file)

    audio_segment = AudioSegment.from_mp3(audio_file)
    normalized_sound = match_target_amplitude(audio_segment, -16.0)

    audio = sr.AudioFile(audio_file)

    r = sr.Recognizer()
    with audio as source:
        r.adjust_for_ambient_noise(source)
        audio_listened = r.record(source)

    # try converting it to text
    whole_text = ""
    try:
        text = r.recognize_sphinx(audio_listened)
    except:
        pass
    else:
        whole_text += text

    if os.path.exists(audio_file):
        os.remove(audio_file)

    return whole_text




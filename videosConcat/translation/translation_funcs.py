from moviepy.editor import *
from moviepy.video import fx


def no_motion(videos):
    # both videos will be combined without any motion
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    return CompositeVideoClip([v_1, v_2.set_start(v_1_time)])


def slide_in_right(videos):
    #motion will be applied from right side
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    return CompositeVideoClip(
        [v_1, v_2.set_start(v_1_time - 1).fx(transfx.slide_in, duration=1, side='right')])


def slide_in_left(videos):
    #motion will be applied from left side
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    return CompositeVideoClip(
        [v_1, v_2.set_start(v_1_time - 1).fx(transfx.slide_in, duration=1, side='left')])


def slide_in_top(videos):
    # motion will be applied from top side
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    return CompositeVideoClip([v_1, v_2.set_start(v_1_time - 1).fx(transfx.slide_in, duration=1, side='top')])


def slide_in_bottom(videos):
    # motion will be applied from bottom side
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    return CompositeVideoClip(
        [v_1, v_2.set_start(v_1_time - 1).fx(transfx.slide_in, duration=1, side='bottom')])


def fade_in(videos):
    #fade in effect will be applied
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    fade = fx.all.fadein(v_1, duration=1, initial_color=None)
    return CompositeVideoClip([fade, v_2.set_start(v_1_time)])

def fade_out(videos):
    #fade out effect will be applied
    v_1 = videos[0]
    v_1_time = v_1.duration
    v_2 = videos[1]
    fade = fx.all.fadeout(v_1, duration=1, final_color=None)
    return CompositeVideoClip([fade, v_2.set_start(v_1_time)])

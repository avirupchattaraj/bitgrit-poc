# Converting a video to mp3 
import moviepy.editor as mp
import os

def video_converter(video_path):
    video_clip=mp.VideoFileClip(video_path)
    video_clip.audio.write_audiofile(r"audio.mp3")
    return os.path.abspath(r"audio.mp3")

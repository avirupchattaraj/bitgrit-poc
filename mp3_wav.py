import pydub
import numpy
import os

def wav_conversion(audio_path):
    #pydub.AudioSegment.ffmpeg = r"C:/ffmpeg"
    sound=pydub.AudioSegment.from_mp3(audio_path)
    sound.export('audio.wav',format='wav')
    return os.path.abspath('audio.wav')
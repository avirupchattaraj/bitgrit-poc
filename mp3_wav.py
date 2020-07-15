import pydub
import numpy
import os


def wav_conversion(audio_path):
    sound = pydub.AudioSegment.from_mp3(audio_path)
    sound.export('./audio/audio.wav', format='wav')
    return os.path.abspath('./audio/audio.wav')

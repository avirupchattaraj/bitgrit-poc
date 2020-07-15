from video_mp3 import video_converter
from mp3_wav import wav_conversion
from speech_text import speech_conversion

if __name__=='__main__':
    video_path=input(r"Enter the path for video")
    audio_path=video_converter(video_path)
    wav_path=wav_conversion(audio_path)
    fvalue=speech_conversion(wav_path)
    print(fvalue)
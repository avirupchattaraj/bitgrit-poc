from video_mp3 import video_converter
from mp3_wav import wav_conversion
from speech_text import speech_conversion
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json


if __name__ == '__main__':
    video_path = "./video/test-video.mp4"
    audio_path = video_converter(video_path)
    wav_path = wav_conversion(audio_path)
    fvalue = speech_conversion(wav_path)

    f = open("./speech-to-text/profile.txt", "w")
    f.write(fvalue)
    f.close()

    # To print the speech-to-text output
    f = open("./speech-to-text/profile.txt", "r")
    print(f.read())

authenticator = IAMAuthenticator('{apikey}')
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator
)

personality_insights.set_service_url(
    '{url}')

with open(join(dirname(__file__), './speech-to-text/profile.txt')) as profile_txt:
    profile = personality_insights.profile(
        profile_txt.read(),
        'application/json',
        content_type='text/plain',
        consumption_preferences=True,
        raw_scores=True
    ).get_result()

    f = open("./personality.json", "w")
    f.write((json.dumps(profile, indent=2)))
    f.close()

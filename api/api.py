from flask import Flask, json, request,redirect,render_template
import os
app=Flask(__name__)
app.config["VIDEO_UPLOAD"]='./bitgrit-poc/video'

def video_converter(video_path):
    video_clip = mp.VideoFileClip(video_path)
    video_clip.audio.write_audiofile(r"./audio/audio.mp3")
    return os.path.abspath(r"./audio/audio.mp3")

# mp3 to wav file conversion
def wav_conversion(audio_path):
    sound = pydub.AudioSegment.from_mp3(audio_path)
    sound.export('./audio/audio.wav', format='wav')
    return os.path.abspath('./audio/audio.wav')

# wav to text file conversion
def speech_conversion(audio_path):
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        val = r.recognize_google(audio)
        return val


@app.route("/video",methods=['POST'])
def get_text_from_video():
    
    # Video input taking and storage
    if request.method=="POST":
        if request.files:
            video=request.files['video']
            video.save(os.path.join(app.config["VIDEO_UPLOAD"],video.filename))
    
    
    # Processing of video starts
    audio_path = video_converter(video_path)
    wav_path = wav_conversion(audio_path)
    fvalue = speech_conversion(wav_path)

    authenticator = IAMAuthenticator('{apikey}')
    personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator)

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

    value=json.dumps(profile,indent=2)
    return value,200


if __name__=='__main__':
    app.run(debug=True)


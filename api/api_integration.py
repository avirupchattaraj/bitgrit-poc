#resume api's imports
from base64 import b64decode, urlsafe_b64decode
import base64
from pyresparser import ResumeParser
import random
import string
import os
from flask import Flask, json, request
from flask_restful import reqparse
from nltk import word_tokenize
#video api's imports
# from video_mp3 import video_converter
# from mp3_wav import wav_conversion
# from speech_text import speech_conversion
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json
import moviepy.editor as mp
import pydub
import speech_recognition as sr
r = sr.Recognizer()

app=Flask(__name__)
@app.route("/resume",methods=['POST'])
def get_contents():
    parser = reqparse.RequestParser()
    parser.add_argument('enc', type=str, location='form')
    args = parser.parse_args()
    content = args['enc']

    #content = request.args.get('enc')
    # print(content)
    # return content
    #
    content_bytes = content.encode()
    content = base64.decodebytes(content_bytes)
    #bytes = base64.urlsafe_b64decode(content)

    if content[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    rand = get_random_string()
    filename = 'resume_'+rand
    outfile = filename+'.pdf'
    #f = open(filename, 'wb')
    # f.write(content)
    # f.close()
    with open(outfile, 'wb') as resume:
        resume.write(content)
    resume.close()
    resume_text = ResumeParser(outfile).get_extracted_data()
    jd = ('Devops JD.pdf')
    jd_text = ResumeParser(jd).get_extracted_data()
    score = findsimilarity(
        listtostr(resume_text['skills']), listtostr(jd_text['skills']))
    print(score)
    return resume_text, 200, {'Content-Type': 'application/json'}


def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(0, 7))
    return result_str


def findsimilarity(X, Y):
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

# sw contains the list of stopwords
    l1 = []
    l2 = []

# remove stop words from the string
    X_set = set(X_list)
    Y_set = set(Y_list)

# form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

# cosine formula
    for i in range(len(rvector)):
        c += l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine


def listtostr(s):
    if not s:
        return " "
    listToStr = ' '.join(map(str, s))
    return listToStr

# movie to mp3 file conversion
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
    pass














if __name__=='__main__':
    app.run(debug=True)
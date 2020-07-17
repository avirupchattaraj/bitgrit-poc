import os
import ffmpy

inputdir = './video/'
outdir = './audio/'

#Direct conversion of .mp4 to .wav, also generation of .wav with same name as of video.

for filename in os.listdir(inputdir):
    actual_filename = filename[:-4]
    if(filename.endswith(".mp4")):
        os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}/{}.wav'.format(filename, outdir, actual_filename))
    else:
        continue

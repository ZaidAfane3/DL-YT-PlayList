import urllib.request
import urllib.error
import traceback
import ffmpeg
import multiprocessing
import re
import sys
import time
import os

from pytube import YouTube, streams
from pytube import Playlist
from datetime import datetime


def findVideoAudio(stream):
    v_index = -1 
    a_index = -1
    for i, v in enumerate(stream):
        v = str(v) 
        if v.find('res="1080p"') != -1:
            v_index = i
            continue
        if v.find('type="audio"') != -1: 
            a_index = i 
            return stream[v_index], stream[a_index]
    
def downloadVideoAudio(stream, name):
    print ('[*] Downloading :', name) 

    stream.download('./videos/temp/', filename = name )
    if '3' in name: 
        os.rename('./videos/temp/3.mp4', './videos/temp/3.mp3')

def mergeVideo(yt):
    print (f'\t [*] Merging Final Video: {yt}')
    a = './videos/temp/3.mp3'
    v = './videos/temp/4.mp4'

    datetimeobject = datetime.strptime(str(yt).split(' ')[-1],'%d/%M/%Y').strftime('%d-%m-%Y')
    out = './videos/[%s] '%(datetimeobject) + 'Machine Learning.mp4'

    # os.system(f'ffmpeg -i {a} -i {v} -c:v -c:a aac {out}')
    os.system(f'ffmpeg -i {"./videos/temp/3.mp3"} -i {"./videos/temp/4.mp4"} -c:v -c:a aac {out}')
    
    # v = ffmpeg.input('./videos/temp/3.mp3')
    # a = ffmpeg.input('./videos/temp/4.mp4') 
    # ffmpeg.output(a , v , out).run()

# def get_streams(playlist):
#     streams = [x.streams.filter(progressive = False, file_extension = "mp4") for x in p.videos]
#     return streams

if __name__ == '__main__': 

    p = Playlist('https://youtube.com/playlist?list=PLxVbB9iWkrnSxFMWVQ40-gjqPzrevzIml')
    for video in p.videos:
        print ('[*] Download :', video.title) 

        stream = video.streams.filter(progressive = False, file_extension = "mp4")
        v, a = findVideoAudio(stream); print (v, a)
        print ('\t [*] Video & Audio Found ')

        v_p = multiprocessing.Process(target=downloadVideoAudio, args=(v, '4.mp4', )) 
        a_p = multiprocessing.Process(target=downloadVideoAudio, args=(a, '3.mp4', )) 
        v_p.start(); a_p.start()
        v_p.join() ; a_p.join()

        print ('\t [*] Video & Audio Downloaded')

        # mergeVideo(video.title)
        print('\t [*] Done')

        exit (0)


exit (0)

for i , v in enumerate(p.videos):
    print (f'[{i+1}] Downloading {p.video_urls[i]}')
    print (*(video.streams().filter(progressive = False, file_extension = 'mp4')), sep='\n')



    v, a = findVideoAudio(video)
    v_p = multiprocessing.Process(target=downloadVideoAudio, args=(v, '4.mp4', )) 
    a_p = multiprocessing.Process(target=downloadVideoAudio, args=(a, '3.mp4', )) 
    
    v_p.start(); a_p.start()
    v_p.join() ; a_p.join()

    exit (2)

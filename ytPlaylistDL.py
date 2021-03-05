from datetime import datetime
from pytube import YouTube
import urllib.request
import urllib.error
import traceback
import ffmpeg
import multiprocessing
import re
import sys
import time
import os

def getPageHtml(url):
    print ('[-] ' + url )
    try:
        yTUBE = urllib.request.urlopen(url).read().decode('utf-8')
        return str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(1)

def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('=') + 1
        pl_id = url[eq_idx:]
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
        return pl_id   
    else:
        print(url, "is not a youtube playlist.")
        exit(1)

def getFinalVideoUrl(vid_urls):
    final_urls = []
    count = 1 
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('http://www.youtube.com/' + vid_url[:url_amp])
        count +=1 
    return final_urls

def getPlaylistVideoUrls(page_content, url):
    playlist_id = getPlaylistUrlID(url)

    vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))

    if vid_url_matches:

        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        print("Found",len(final_vid_urls),"videos in playlist.")
        # printUrls(final_vid_urls)
        return final_vid_urls
    else:
        print('No videos found.')
        exit(1)

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
            return v_index, a_index
    
def downloadVideoAudio(stream, name):
    stream.download('./videos/temp/', filename = name )
    if '3' in name: 
        os.rename('./videos/temp/3.mp4', './videos/temp/3.mp3')

def mergeVideo(yt):
    print (f'[*] Merging Final Video: {yt.title}')
    a = './videos/temp/3.mp3'
    v = './videos/temp/4.mp4'

    datetimeobject = datetime.strptime(str(yt.title).split(' ') [3],'%d/%m/%Y').strftime('%d-%m-%Y')
    out = './videos/[%s] ' + 'Machine Learning.mp4'%(datetimeobject)
    os.system(f'ffmpeg -i {a} -i {v} -c:v -c:a aac {out}')

    # v = ffmpeg.input('./videos/temp/3.mp3')
    # a = ffmpeg.input('./videos/temp/4.mp4') 
    # ffmpeg.output(a , v , out).run()

def download_Video_Audio(path, vid_url, file_no):
    try:
        yt = YouTube(vid_url)
    except Exception as e:
        print("Error:", str(e), "- Skipping Video with url '"+vid_url+"'.")
        return

    video = yt.streams.filter(progressive = False, file_extension = "mp4").all()
    








if __name__ == '__main__':

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('USAGE: python ytPlaylistDL.py playlistURL OR python ytPlaylistDL.py playlistURL destPath')
        exit(1)
    else:
        url = sys.argv[1]
        url = 'youtube.com/playlist?list=PLxVbB9iWkrnSxFMWVQ40-gjqPzrevzIml'
        directory = os.getcwd() if len(sys.argv) != 3 else sys.argv[2]
    
        # make directory if dir specified doesn't exist
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(e)
            exit(1)

        if not url.startswith("http"):
            pass
            url = 'https://' + url

        playlist_page_content = getPageHtml(url)
        vid_urls_in_playlist = getPlaylistVideoUrls(playlist_page_content, url)

        # downloads videos and audios
        for i,vid_url in enumerate(vid_urls_in_playlist):
            download_Video_Audio(directory, vid_url, i)
            time.sleep(1)

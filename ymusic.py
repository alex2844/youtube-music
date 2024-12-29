#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, re, json, youtube_dl
from getopt import getopt
from datetime import datetime
from ytmusicapi import YTMusic
from ytmusicapi.setup import setup, setup_oauth
from ytmusicapi.ytmusic import OAuthCredentials
from mutagen.id3 import ID3, APIC, TPE1, TALB, TIT2, TYER, TDRC, COMM

version = '2.0.0'
limit = 100000
ytmusic = YTMusic()

def auth():
    global ytmusic
    config = {'auth':'headers'}
    filepath = "config.json"
    if os.path.exists(filepath):
        with open(filepath) as f:
            config = json.load(f)
        filepath = config['auth'] + ".json"
        if not os.path.exists(filepath):
            if config['auth'] == 'oauth':
                setup_oauth(
                    client_id = config['oauth']['client_id'],
                    client_secret = config['oauth']['client_secret'],
                    filepath = filepath
                )
            elif config['auth'] == 'headers':
                setup(
                    filepath = filepath,
                    headers_raw = "\n".join([f"{key}: {value}" for key, value in config['headers'].items()])
                )
    else:
        filepath = config['auth'] + ".json"
        setup(
            filepath = filepath
        )
    if config['auth'] == 'oauth':
        ytmusic = YTMusic(
            filepath,
            oauth_credentials = OAuthCredentials(
                client_id = config['oauth']['client_id'],
                client_secret = config['oauth']['client_secret']
            )
        )
    else:
        ytmusic = YTMusic(filepath)

def download_track(id, info=None):
    if info is None:
        info = ytmusic.get_watch_playlist(get_id(id))['tracks'][0]
    fname = re.sub('[^-а-яА-Яa-zA-Z0-9_.()\s]+', '', info['title'])
    fname = re.sub(r"\.+", " ", fname).strip('.')
    fname = re.sub(r"\s+", " ", fname).strip()
    if not os.path.exists(fname+'.mp3'):
        print('[youtube-music] Starting: '+fname)
        with youtube_dl.YoutubeDL({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0'
            }],
            'writeinfojson': True,
            'writethumbnail': True,
            'outtmpl': fname+'.%(etx)s',
            'outtmpl_na_placeholder': 'NA'
        }) as ydl:
            ydl.download([id])
        id3 = ID3(fname+'.mp3')
        if os.path.exists(fname+'.NA.info.json'):
            with open(fname+'.NA.info.json') as f:
                info = json.load(f)
                os.remove(fname+'.NA.info.json')
        if os.path.exists(fname+'.NA.jpg'):
            with open(fname+'.NA.jpg', 'rb') as albumart:
                id3['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, desc=info['title'],
                    data=albumart.read()
                )
            os.remove(fname+'.NA.jpg')
        id3['TIT2'] = TIT2(encoding=3, text=info['title'])
        if 'artist' in info:
            id3['TPE1'] = TPE1(encoding=3, text=info['artist'])
        if 'album' in info:
            id3['TALB'] = TALB(encoding=3, text=info['album'])
        if 'release_year' in info:
            id3['TYER'] = TYER(encoding=3, text=str(info['release_year']))
        if 'release_date' in info:
            id3['TDRC'] = TDRC(encoding=3, text=datetime.strptime(info['release_date'], "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%S"))
        id3['COMM'] = COMM(encoding=3, lang='eng', desc='desc', text='https://music.youtube.com/watch?v='+id)
        id3.save()
    else:
        print('[youtube-music] Skiping: '+fname)

def download_playlist(id, notSkipErrors=False):
    try:
        tracks = get_tracks(id)
    except:
        auth()
        tracks = get_tracks(id)
    for track in tracks:
        if track['videoId'] is not None:
            if notSkipErrors is False:
                try:
                    download_track(track['videoId'], track)
                except KeyboardInterrupt:
                    exit()
                except:
                    print('Error: vid: '+track['videoId'])
            else:
                download_track(track['videoId'], track)
    print('[youtube-music] Finish')

def get_id(url):
    if re.match(r"^https://((www\.|music\.)?youtube\.com|youtu.be)/", url):
        if "list=" in url:
            match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
            if match:
                return match.group(1)
        elif "v=" in url:
            match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
            if match:
                return match.group(1)
        elif "youtu.be/" in url:
            match = re.search(r"youtu.be/([a-zA-Z0-9_-]+)", url)
            if match:
                return match.group(1)
    return url

def get_tracks(id):
    if id is None:
        res = ytmusic.get_liked_songs(limit)
    else:
        res = ytmusic.get_playlist(get_id(id), limit)
    return res['tracks']

def main(args):
    opt = ['help', 'version', 'liked', 'playlist=', 'track=', 'not-skip-error']
    arguments, values = getopt(args, 'hvdao:p:s', opt)
    if len(arguments) == 0:
        arguments = [('-h', '')]
    for current_argument, current_value in arguments:
        if current_argument in ('-h', '--help'):
            print('\n'.join([
                '-h, --help             Print help',
                '-v, --version          Print program version',
                '-l, --liked            Download all liked songs',
                '-p, --playlist ID      Download playlist',
                '-t, --track ID         Download one track',
                '--not-skip-error       Not skip error'
            ]))
        elif current_argument in ('-v', '--version'):
            print('[youtube-music] Version: '+version)
        elif current_argument in ('-l', '--liked'):
            download_playlist(None, ('--not-skip-error' in args))
        elif current_argument in ('-p', '--playlist'):
            download_playlist(current_value, ('--not-skip-error' in args))
        elif current_argument in ('-t', '--track'):
            download_track(current_value)

if __name__ == "__main__":
    main(sys.argv[1:])
    # main(os.environ.get('args').split(' '))

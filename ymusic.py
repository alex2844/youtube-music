#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt, os, sys, json, youtube_dl
from ytmusicapi import YTMusic
from mutagen.id3 import ID3, TPE1, TIT2, TRCK, TALB, APIC

if os.environ.get('COLAB_GPU', False):
    if not os.path.exists('/content/drive/ymusic'):
        os.mkdir('/content/drive/ymusic')
    os.chdir('/content/drive/ymusic')

version = '1.5.0'
def auth():
    print('Cookie:SID: <<-- https://music.youtube.com/ => DevTools => Application => Cookies => Value')
    cookie_sid = str(input())
    if not cookie_sid:
        sys.exit("exit: empty cookie")
    print('Cookie:HSID:')
    cookie_hsid = str(input())
    if not cookie_hsid:
        sys.exit("exit: empty cookie")
    print('Cookie:SSID')
    cookie_ssid = str(input())
    if not cookie_ssid:
        sys.exit("exit: empty cookie")
    print('Cookie:APISID:')
    cookie_apisid = str(input())
    if not cookie_apisid:
        sys.exit("exit: empty cookie")
    print('Cookie:SAPISID:')
    cookie_sapisid = str(input())
    if not cookie_sapisid:
        sys.exit("exit: empty cookie")
    with open(os.path.expanduser("~/.ymusic.json"), 'w') as f:
        json.dump({
            'User-Agent': 'Mozilla/5.0 (X11; CrOS aarch64 13020.54.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.77 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'X-Goog-AuthUser': '0',
            'x-origin': 'https://music.youtube.com',
            'Cookie': '; '.join([
                'SID='+cookie_sid,
                'HSID='+cookie_hsid,
                'SSID='+cookie_ssid,
                'APISID='+cookie_apisid,
                'SAPISID='+cookie_sapisid
            ])
        }, f)

def all():
    if not os.path.exists(os.path.expanduser("~/.ymusic.json")):
        auth()
    ytmusic = YTMusic(os.path.expanduser("~/.ymusic.json"))
    liked = ytmusic.get_liked_songs()
    for song in liked['tracks']:
        if not os.path.exists(song['title']+'.mp3'):
            one(song['videoId'], song['title'])
            audio = ID3(song['title']+'.mp3')
            with open(song['title']+'.jpg', 'rb') as albumart:
                audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, desc=song['title'],
                    data=albumart.read()
                )
            os.remove(song['title']+'.jpg')
            if song['artists'] is not None:
                audio['TPE1'] = TPE1(encoding=3, text=song['artists'][0]['name'])
            if song['album'] is not None:
                audio['TALB'] = TALB(encoding=3, text=song['album']['name'])
            audio['TIT2'] = TRCK(encoding=3, text=song['title'])
            audio.save()
        else:
            print('[youtube-music] Skiping: '+song['title'])
    print('Finish')

def one(id, title=None):
    if title is None:
        title = id
    print('[youtube-music] Starting: '+title)
    with youtube_dl.YoutubeDL({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0'
        }],
        'writethumbnail': True,
        'outtmpl': title+'.%(etx)s',
    }) as ydl:
        ydl.download(['https://www.youtube.com/watch?v='+id])

def sync():
    os.system('adb push --sync ./* /sdcard/Music')

if __name__ == "__main__":
    arguments, values = getopt.getopt(sys.argv[1:], 'hvao:s', ['help', 'version', 'auth', 'all', 'one=', 'sync'])
    if len(arguments) is 0:
        if os.environ.get('COLAB_GPU', False):
            arguments = [('-a', '')]
        else:
            arguments = [('-h', '')]
    for current_argument, current_value in arguments:
        if current_argument in ('-h', '--help'):
            print('\n'.join([
                '-h, --help             Print help',
                '-v, --version          Print program version',
                '--auth                 Authorization',
                '-a, --all              Download all liked songs',
                '-o, --one ID           Download one song',
                '-s, --sync             Sync with android phone'
            ]))
        elif current_argument in ('-v', '--version'):
            print('[youtube-music] Version: '+version)
        elif current_argument in ('-a', '--all'):
            all()
        elif current_argument in ('-o', '--one'):
            one(current_value)
        elif current_argument in ('--auth'):
            auth()
        elif current_argument in ('-s', '--sync'):
            sync()

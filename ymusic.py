#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt, os, sys, json, getpass, re, youtube_dl
from ytmusicapi import YTMusic
from ytmusicapi.setup import setup_oauth
from mutagen.id3 import ID3, APIC, TPE1, TALB, TIT2, COMM

version = '1.7.2'
limit = 100000
def auth():
    oauth = setup_oauth(os.path.expanduser("oauth.json"))

def download(id, title=None):
    if re.match(r"^https://", id):
        id = id.split('v=')[1].split('&')[0]
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

def foreach(song, fname):
    download(song['videoId'], fname)
    audio = ID3(fname+'.mp3')
    if os.path.exists(fname+'.jpg'):
        with open(fname+'.jpg', 'rb') as albumart:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=song['title'],
                data=albumart.read()
            )
        os.remove(fname+'.jpg')
    if song['artists'] is not None:
        audio['TPE1'] = TPE1(encoding=3, text=song['artists'][0]['name'])
    if song['album'] is not None:
        audio['TALB'] = TALB(encoding=3, text=song['album']['name'])
    audio['TIT2'] = TIT2(encoding=3, text=song['title'])
    audio['COMM'] = COMM(encoding=3, lang='eng', desc='desc', text='https://music.youtube.com/watch?v='+song['videoId'])
    audio.save()

def playlist(id, doubles=False, skipErrors=False, noSubfolder=False):
    if os.environ.get('COLAB_RELEASE_TAG', False):
        skipErrors=True
    if id is None:
        if not os.path.exists(os.path.expanduser("oauth.json")):
            auth()
        list = YTMusic(os.path.expanduser("oauth.json")).get_liked_songs(limit)
    else:
        if re.match(r"^https://", id):
            id = id.split('list=')[1]
        try:
            list = YTMusic().get_playlist(id, limit)
        except:
            if not os.path.exists(os.path.expanduser("oauth.json")):
                auth()
            list = YTMusic(os.path.expanduser("oauth.json")).get_playlist(id, limit)
    if doubles is False:
        for song in list['tracks']:
            if song['videoId'] is not None:
                fname = re.sub('[^-а-яА-Яa-zA-Z0-9_.() ]+', '', song['title']).strip()
                if song['album'] is not None and not noSubfolder:
                    fname = os.path.join(re.sub('[^-а-яА-Яa-zA-Z0-9_.() ]+', '', song['album']['name']).strip(), fname)
                if not os.path.exists(fname+'.mp3'):
                    if skipErrors is False:
                        foreach(song, fname)
                    else:
                        try:
                            foreach(song, fname)
                        except KeyboardInterrupt:
                            exit()
                        except:
                            print('Error: vid: '+song['videoId'])
                else:
                    print('[youtube-music] Skiping: '+fname)
        print('Finish')
    else:
        titles = []
        ids = []
        for song in list['tracks']:
            if song['videoId'] is not None:
                id = song['videoId']
                title = song['title'].split(' [')[0].split(' (')[0]
                if title in titles:
                    print('\n'+title)
                    print('https://music.youtube.com/watch?v='+ids[titles.index(title)])
                    print('https://music.youtube.com/watch?v='+id)
                else:
                    titles.append(title)
                    ids.append(id)

def sync():
    os.system('adb push --sync ./* /sdcard/Music')

def main(args):
    opt = ['help', 'version', 'doubles', 'skip-error', 'colab', 'all', 'one=', 'playlist=', 'sync', 'no-subfolder']
    arguments, values = getopt.getopt(args, 'hvdao:p:s', opt)
    if len(arguments) == 0:
        if os.environ.get('COLAB_RELEASE_TAG', False):
            arguments = [('--colab', '')]
        else:
            arguments = [('-h', '')]
    for current_argument, current_value in arguments:
        if current_argument in ('-h', '--help'):
            print('\n'.join([
                '-h, --help             Print help',
                '-v, --version          Print program version',
                '-d, --doubles          Show doubles',
                '--skip-error           Skip error',
                '--colab                Colab menu',
                '--no-subfolder         Don\'t output songs to subfolders named as album',
                '-a, --all              Download all liked songs',
                '-o, --one ID           Download one song',
                '-p, --playlist ID      Download playlist',
                '-s, --sync             Sync with android phone'
            ]))
        elif current_argument in ('-v', '--version'):
            print('[youtube-music] Version: '+version)
        elif current_argument in ('-a', '--all'):
            playlist(None, ('-d' in args) or ('--doubles' in args), ('--skip-error' in args), ('--no-subfolder' in args))
        elif current_argument in ('-o', '--one'):
            download(current_value)
        elif current_argument in ('-p', '--playlist'):
            playlist(current_value, ('-d' in args) or ('--doubles' in args), ('--skip-error' in args), ('--no-subfolder' in args))
        elif current_argument in ('-s', '--sync'):
            sync()
        elif current_argument in ('--colab'):
            opt = list(filter(lambda v : v not in ('help', 'doubles', 'skip-error', 'auth', 'load-cookies=', 'colab', 'sync', 'no-subfolder'), opt))
            for k, v in enumerate(opt, start=1):
                print(k, v.replace('=', ''))
            sel = opt[int(input()) - 1];
            args = [ '--'+sel.replace('=', '') ]
            if sel[-1] == '=':
                args.append(str(input('ID: ')))
            main(args)

if __name__ == "__main__":
    main(sys.argv[1:])

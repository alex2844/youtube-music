if [[ ! -z `type -p apt` ]]; then
	if [[ -z `type -p python3` || -z `type -p pip3` || -z `type -p ffmpeg` ]]; then
		sudo apt install python3 python3-pip ffmpeg
	fi
fi
if ! (stat -t /usr/local/lib/python3*/dist-packages/{ytmusicapi,youtube_dl,mutagen} > /dev/null 2>&1) then
	sudo pip3 install ytmusicapi youtube-dl mutagen
fi
if ! (stat -t /usr/local/lib/python*/dist-packages/google/colab > /dev/null 2>&1) then
	sudo $(echo $([ `type -p curl` ] && echo "curl -s" || echo "wget -q -O -")" https://raw.githubusercontent.com/alex2844/youtube-music/master/ymusic.py") > 'test.py'
	sudo chmod +x /usr/local/bin/ymusic;
fi

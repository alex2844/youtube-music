# youtube-music

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alex2844/youtube-music/blob/master/ymusic.ipynb 'Open In Colab')

## Скачивание треков из Youtube Music

#### Справка
```
:$ ymusic --help
-h, --help             Print help
-v, --version          Print program version
-l, --liked            Download all liked songs
-p, --playlist ID      Download playlist
-t, --track ID         Download one track
--not-skip-error       Not skip error
```

#### Запуск на локальной машине
```bash
python -m pip install -r requirements.txt
python ymusic.py
```

#### Запуск в Colab (Например если не хотите ставить python)
* Нажмите на значок с надписью 'Открыть в Colab'
* Запустите (Runtime -> Run all)
После завершения загрузки, загруженные файлы будут находиться на вашем google диске в папке с именем 'ymusic'

## Downloads songs from Youtube Music

## Youtube
| [![track][track_img]][track_url] | [![playlist][playlist_img]][playlist_url]
| --- | ---

[track_img]: https://img.youtube.com/vi/k6GZlTG5RFI/0.jpg "Скачивание треков из Youtube Music в google drive"
[track_url]: https://youtu.be/k6GZlTG5RFI
[playlist_img]: https://img.youtube.com/vi/L02LzD5rAXg/0.jpg "Скачивание плейлистов из Youtube Music в google drive"
[playlist_url]: https://youtu.be/L02LzD5rAXg

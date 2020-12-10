# youtube-music

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alex2844/youtube-music/blob/master/ymusic.ipynb 'Open In Colab')

## Скачивание треков из Youtube Music

#### Справка
```
:$ ymusic --help
-h, --help             Print help
-v, --version          Print program version
-d, --doubles          Show doubles
--skip-error           Skip error
--colab                Colab menu
--auth                 Authorization
--load-cookies FILE    Use cookies file
--no-subfolder         Don\'t output songs to subfolders named as album
-a, --all              Download all liked songs
-o, --one ID           Download one song
-p, --playlist ID      Download playlist
-s, --sync             Sync with android phone
```

#### Авторизация через cookie файл
- Скачиваем расширение CorsProxy (https://alex2844.github.io/js-global-fetch/index.html?extension)
- Заходим на страницу с расширениями (chrome://extensions/)
- Включаем режим разработчика
- Загрузить распакованное расширение
- Жмем на иконку расширения правой кнопкой мыши
- Save cookies

#### Установка на локальную машину (Например ubuntu)
```bash
curl -sL https://raw.githubusercontent.com/alex2844/youtube-music/master/install.sh | sudo -E bash -
```

#### Запуск в Colab (Например если не хотите ставить python)
* Нажмите на значок с надписью 'Открыть в Colab'
* Запустите (Runtime -> Run all)
После завершения загрузки, загруженные файлы будут находиться на вашем google диске в папке с именем 'ymusic'

## Downloads songs from Youtube Music

#### Youtube
###### Скачивание треков из Youtube Music на компьютер
[![Youtube](https://img.youtube.com/vi/9d4cW0MACXA/0.jpg)](https://www.youtube.com/watch?v=9d4cW0MACXA 'Youtube: Скачивание треков из Youtube Music на компьютер')
###### Скачивание треков из Youtube Music в google drive
[![Youtube](https://img.youtube.com/vi/k6GZlTG5RFI/0.jpg)](https://www.youtube.com/watch?v=k6GZlTG5RFI 'Youtube: Скачивание треков из Youtube Music в google drive')
###### Скачивание плейлистов из Youtube Music в google drive
[![Youtube](https://img.youtube.com/vi/L02LzD5rAXg/0.jpg)](https://www.youtube.com/watch?v=L02LzD5rAXg 'Youtube: Скачивание плейлистов из Youtube Music в google drive')

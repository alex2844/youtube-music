# YouTube Music

> Sync your YouTube Music playlists to MP3 with correct tags and cover art.

This script allows you to easily download and synchronize music from YouTube and
YouTube Music. It uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) with
optimized settings to ensure high-quality audio and correct metadata.

The script is designed to be a powerful sync tool. Running it in **Google Colab**
allows you to maintain a mirrored copy of your "Liked Music" directly on your
Google Drive or download it as a ZIP archive.

It automatically handles metadata parsing, cover art embedding, and cleaning up
filenames for universal compatibility.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)][notebook]

## Features

* **Smart Synchronization**: When downloading a playlist (e.g., "Liked Music"),
  the script downloads new tracks and **automatically deletes** local files
  that were removed from the playlist.
* **High Quality Audio**: Uses the Android API to fetch high-quality audio streams
  (Opus/M4A) and converts them to MP3 (V0) without transcoding glitches.
* **Metadata & Tags**: Automatically parses "Artist - Title", removes junk like
  " - Topic", and embeds cover art directly into the MP3 file.
* **Google Drive Sync**: In Colab, it syncs your music library directly to
  Google Drive.
* **Browser Cookies**: Support for loading cookies directly from your browser
  to bypass age restrictions or download Premium content.
* **Zip Drive Mode**: A special Colab mode to zip and download your existing
  Google Drive music collection to your phone without re-downloading tracks.
* **Clean Filenames**: Generates safe filenames compatible with all operating
  systems and car audio players.

## Usage

### Local

1. Install the necessary dependencies (ffmpeg, python3, yt-dlp).
2. Make [`ymusic.sh`][script] executable: `chmod +x ymusic.sh`.
3. Run the script:

    ```bash
    ./ymusic.sh [OPTIONS] <URL>
    ```

    **Options:**

    * `-h, --help`: Show help message.
    * `-v, --version`: Show script version.
    * `-c, --cookies=<path>`: Path to Netscape formatted cookies file.
    * `-b, --browser=<name>`: Load cookies from browser (chrome, firefox, edge).
    * `-o, --output=<path>`: Output directory.
    * `-4, --ipv4`: Force IPv4 connection.
    * `--temp-dir=<path>`: Temporary directory for downloads.

    **Examples:**

    Download a single track:

    ```bash
    ./ymusic.sh "https://music.youtube.com/watch?v=VIDEO_ID"
    ```

    Sync "Liked Music" playlist using Chrome cookies (downloads new, deletes
    removed):

    ```bash
    ./ymusic.sh -b chrome "https://music.youtube.com/playlist?list=LM"
    ```

### Google Colab

1. Open the [`ymusic.ipynb`][notebook] file in Google Colab.
2. Fill in the parameters in the "Settings" block.
3. Choose the `SAVE` mode:
    * `save`: Syncs directly to your Google Drive (`/ymusic` folder).
    * `download`: Downloads tracks and zips them for browser download.
    * `zip_drive`: Zips your existing Google Drive collection for download
      (no YouTube traffic).
4. Run the cells.

## Installing Dependencies

If you don't have dependencies installed locally, you can use the
`INSTALL_DEPENDENCIES=true` variable to attempt auto-installation.

```bash
INSTALL_DEPENDENCIES=true ./ymusic.sh [OPTIONS] <URL>
```

---

### Синхронизируйте музыку с YouTube с правильными тегами и обложками

Этот скрипт позволяет легко скачивать и синхронизировать музыку с YouTube и
YouTube Music. Он использует [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) с
оптимизированными настройками для получения лучшего качества звука и
метаданных.

Скрипт разработан как мощный инструмент синхронизации. Запуск в
**Google Colab** позволяет хранить зеркальную копию плейлиста "Понравившееся"
прямо на Google Диске или скачивать его в виде ZIP-архива.

Он автоматически обрабатывает метаданные, вшивает обложки альбомов и очищает
имена файлов для совместимости с любыми устройствами.

## Возможности

* **Умная синхронизация**: При скачивании плейлиста (например, "Liked Music"),
  скрипт скачивает новые треки и **автоматически удаляет** локальные файлы,
  которые были убраны из плейлиста.
* **Высокое качество**: Использует Android API для получения качественных
  потоков (Opus/M4A) и конвертирует их в MP3 (V0) без сбоев.
* **Метаданные и теги**: Умный парсинг "Артист - Название", удаление мусора
  вроде " - Topic" и встраивание обложки прямо в файл MP3.
* **Синхронизация с Google Drive**: В Colab скрипт синхронизирует вашу
  музыкальную библиотеку напрямую с Google Диском.
* **Cookies из браузера**: Поддержка загрузки куков напрямую из браузера
  для обхода возрастных ограничений или скачивания Premium контента.
* **Режим Zip Drive**: Специальный режим в Colab для упаковки существующей
  коллекции с Google Диска в ZIP и скачивания на телефон без повторной
  загрузки треков с YouTube.
* **Чистые имена файлов**: Генерация безопасных имен файлов, совместимых со
  всеми ОС и автомобильными магнитолами.

## Использование

### Локально

1. Установите необходимые зависимости (ffmpeg, python3, yt-dlp).
2. Сделайте [`ymusic.sh`][script] исполняемым: `chmod +x ymusic.sh`.
3. Запустите скрипт:

    ```bash
    ./ymusic.sh [ОПЦИИ] <URL>
    ```

    **Опции:**

    * `-h, --help`: Показать справку.
    * `-v, --version`: Показать версию скрипта.
    * `-c, --cookies=<path>`: Путь к файлу cookies (Netscape format).
    * `-b, --browser=<name>`: Загрузить cookies из браузера (chrome, firefox,
      edge).
    * `-o, --output=<path>`: Папка для сохранения.
    * `-4, --ipv4`: Принудительно использовать IPv4.
    * `--temp-dir=<path>`: Временная папка для загрузок.

    **Примеры:**

    Скачивание одного трека:

    ```bash
    ./ymusic.sh "https://music.youtube.com/watch?v=VIDEO_ID"
    ```

    Синхронизация плейлиста "Понравившееся" с использованием куков Chrome
    (скачивание новых, удаление удаленных):

    ```bash
    ./ymusic.sh -b chrome "https://music.youtube.com/playlist?list=LM"
    ```

### Запуск в Google Colab

1. Откройте файл [`ymusic.ipynb`][notebook] в Google Colab.
2. Заполните параметры в блоке "Settings".
3. Выберите режим `SAVE`:
    * `save`: Синхронизация напрямую с Google Drive (папка `/ymusic`).
    * `download`: Скачивание треков и упаковка в ZIP для браузера.
    * `zip_drive`: Упаковка существующей коллекции с Google Drive в ZIP для
      скачивания (без трафика с YouTube).
4. Запустите ячейки.

## Установка Зависимостей

Если зависимости не установлены, можно использовать переменную
`INSTALL_DEPENDENCIES=true` для их автоматической установки.

```bash
INSTALL_DEPENDENCIES=true ./ymusic.sh [ОПЦИИ] <URL>
```

---

## Youtube

| [![track][track_img]][track_url] | [![playlist][playlist_img]][playlist_url]
| --- | ---

[track_img]: https://img.youtube.com/vi/k6GZlTG5RFI/0.jpg "Скачивание треков"
[track_url]: https://youtu.be/k6GZlTG5RFI
[playlist_img]: https://img.youtube.com/vi/L02LzD5rAXg/0.jpg "Скачивание плейлистов"
[playlist_url]: https://youtu.be/L02LzD5rAXg
[script]: https://raw.githubusercontent.com/alex2844/youtube-music/v3.0.0/ymusic.sh "Open script"
[notebook]: https://colab.research.google.com/github/alex2844/youtube-music/blob/v3.0.0/ymusic.ipynb "Open In Colab"

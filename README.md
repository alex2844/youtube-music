# youtube-music

## Installation
## Установка
```
git clone https://github.com/alex2844/youtube-music.git && cd youtube-music && npm install
```

## Get playlist
## Получить плейлист
### Open playlist on music.youtube.com and paste code to DevTools (Ctrl+Shift+J)
### Откройте плейлист на сайте music.youtube.com и вставьте код в DevTools (Ctrl+Shift+J)
```javascript
document.body.append(Object.assign(document.createElement('script'), {
	src: 'https://cdn.jsdelivr.net/gh/alex2844/youtube-music/index.js',
	onload: e => e.target.remove()
}))
```

## Download playlist
## Скачать плейлист
```javascript
npm start
```

## Sync playlist to android (adb)
## Синхранизация плейлиста с android (adb)
```javascript
npm run sync
```

## TODO
- Возможно откажусь от сторонего сервиса
- Докачивание
- При скачивании удалять отсутствующие в плейлисте треки
- При синхранизации удалять старый плейлист
- ID3
- Создание каталога files из самого приложения
- Бинарники

# Changelog

| Key           | Description                                   | Описание
|---            |---                                            |---
| Added         | Added for new features                        | Добавлено для новых функций
| Changed       | Changed for changes in existing functionality | Изменено для изменений в существующей функциональности
| Deprecated    | Deprecated for soon-to-be removed features    | Устарело для функций, которые скоро будут удалены
| Removed       | Removed for now removed features              | Удалено для удалённых функций
| Fixed         | Fixed for any bug fixes                       | Исправлено для любых исправлений
| Security      | Security in case of vulnerabilities           | Безопасность в случае уязвимостей


## [Unreleased](../../compare/2.0.0...HEAD)

## [2.0.0](../../releases/tag/2.0.0) - 2024-12-29
### Added
* Форма настроек для google colab
* Авторизация используя headers и oauth
* Выбор в каком виде хранить на google drive: zip, либо mp3
* Файлы конфигурации хранятся в google drive, для того чтоб при последующем запуске - они же и использовались

## [1.7.1] - 2023-11-04
### Changed
* Заменил авторизацию по cookies на oauth

## [1.6.0](../../releases/tag/v1.6.0) - 2020-12-11
### Added
* Авторизация через cookie файл (--load-cookies FILE)
* Не создавать директории для альбомов (--no-subfolder)
### Fixed
* Cookie:__Secure-3PAPISID

## [1.5.2](../../releases/tag/v1.5.2) - 2020-06-09
### Added
* Директории для альбомов
* Поиск дублей в плейлисте
* Пропуск ошибок (--skip-error)
### Fixed
* Название трека прописывается в поле номера трека

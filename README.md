# S3-API

API для взаимодействия в s3-хранилищем.

API коннектится к s3-бакету, указанному в .env-файлу.

Функционал заклюсается в скачивании картинки из бакета, ресайзинга и загрузки обратно, с возможностью выбора папки для загрузки, или создания новой.

Возможность отслеживать статус обработки картинки

Ваш .env файл должен выглядеть вот так
```
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=db
POSTGRES_USER=
POSTGRES_PASSWORD=


AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_ENDPOIN_URL=
AWS_REGION = 'ru-central1'
S3_BUCKET=
```
после просто запускается docker compose командой:
```
docker compose run
```

После заруска приложения переходите на localhost и пользуетесь API)

Версии фоток:

Original

thumb: 150x120, to_fit

big_thumb: 700x700, to_fit

big_1920, 1920x1080, to_fit

d2500: 2500x2500, to_fit

to_fit - ресайзится по длинной стороне.

Стэк:

Python,  FastAPI
PostgreSQL
YandexCloud как s3-хранилище(возможно будет работать и с другими, но это не точно)
Websockets
Docker

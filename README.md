# Multistreamer
Кратко: опенсорсный restream.io с приправами

Развёрнуто: Stream-сервер с web-интерфейсом, способный:
- Принимать аудио/видео поток в форматах rtmp, rtsp, hls
- ретранслировать поток на сервисы youtube, webinar.ru
- перекодировать поток на лету из входного разрешения в заданное 
- поддерживать не менее трёх выходных разрешений (480p, 720p, 1080p) 
- сохранять несжатый поток в файл на жёстком диске
- по запросу осуществлять захват потока из webinar'а (с чатом и окном преподавателя) и сохранять его на диск. Возможно даже не в виде изображения, а виде метаданных, но в финале - рендерить его в видеофайл вместе с исходным видеопотоком.
- отображать в режиме реального времени текущую загрузку процессора/видеокарты/жёсткого диска/сети
- создавать youtube- и webinar-трансляцию прямо из интерфейса системы

## Технологический стек:
- Python 3
- Django 3

## Quickstart
```bash
sudo apt install make
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
./manage.py runserver
```

## Read more
- FFMpeg: [https://ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)
- ffmpeg-python: [https://github.com/kkroening/ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

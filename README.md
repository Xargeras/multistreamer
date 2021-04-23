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
- Docker


## Установка Docker
```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt-get update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
newgrp docker
```

## Quickstart
```bash
sudo apt install make
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
./manage.py runserver
```
Для автоматического запуска `rtsp-server` добавить опцию `runrtsp` в конфигурацию запуска

## Read more
- FFMpeg: [https://ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)

Для запуска видеопотока с помощью ffmpeg:
```bash
ffmpeg -re -stream_loop -1 -i file.ts -c copy -f rtsp rtsp://localhost:8554/mystream
ffmpeg -re -stream_loop -1 -i file.ts -c copy -f flv rtmp://localhost/mystream
```

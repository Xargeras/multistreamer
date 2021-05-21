FROM ubuntu:latest
MAINTAINER Andrew Smirnov <smirnov@informatics.ru>

ADD ./ /ps102_multistreamer
WORKDIR /ps102_multistreamer/
RUN apt-get update && apt-get install -y build-essential nano python3 python3-dev python3-pip default-libmysqlclient-dev supervisor ffmpeg
RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir -p /var/log/supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD exec /usr/bin/supervisord --nodaemon

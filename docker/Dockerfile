FROM python:3.8
MAINTAINER Andrew Smirnov <smirnov@informatics.ru>
ADD ./ /ps102_multistreamer
WORKDIR /ps102_multistreamer/
RUN apt-get update && apt-get install -y build-essential nano python3-dev default-libmysqlclient-dev
RUN pip install --no-cache-dir -r ./requirements.txt
CMD exec ./docker/run.sh

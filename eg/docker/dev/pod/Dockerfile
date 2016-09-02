FROM ubuntu:xenial
MAINTAINER mobo

ENV DEBIAN_FRONTEND noninteractive

# Install ubuntu packages
RUN apt-get update
RUN apt-get install -y python python-dev python-pip wget g++ libmysqlclient-dev \
    graphviz libgraphviz-dev pkg-config libldap2-dev libsasl2-dev \
    libssl-dev libjpeg-dev python-imaging libfreetype6-dev python-chardet \
    python-fpconst python-apt python-debian python-debianbts python-reportbug \
    python-soappy memcached gettext

# Compile ffmpeg
WORKDIR /usr/local/
RUN wget http://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
RUN tar -Jxvf ffmpeg-release-64bit-static.tar.xz
RUN rm -f ffmpeg-release-64bit-static.tar.xz
RUN mv ffmpeg-*-64bit-static ffmpeg
RUN ln -s /usr/local/ffmpeg/ffmpeg /usr/local/bin/ffmpeg
RUN ln -s /usr/local/ffmpeg/ffmpeg-10bit /usr/local/bin/ffmpeg-10bit
RUN ln -s /usr/local/ffmpeg/ffprobe /usr/local/bin/ffprobe
RUN ln -s /usr/local/ffmpeg/ffserver /usr/local/bin/ffserver
RUN ln -s /usr/local/ffmpeg/qt-faststart /usr/local/bin/qt-faststart

# Install python packages
RUN  mkdir -p /usr/local/src
WORKDIR /usr/local/src
ADD requirements.txt /usr/local/src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# # Add code folder
# ADD code /code
WORKDIR /code
# RUN pip install --upgrade pip
# RUN pip install -r requirements/dev.txt

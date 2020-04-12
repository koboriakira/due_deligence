# docker build -t due_deligence_image .
FROM python:3.7.5-slim

WORKDIR /docker_image

# 必要なパッケージをインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y \
  default-mysql-server \
  default-libmysqlclient-dev \
  vim \
  gcc

# mysqlの設定
ADD ./docker/mysql mysql
RUN service mysql start \
  && mysql -uroot < mysql/init.ddl \
  && mysql -uroot db < mysql/create_document.sql \
  && mysql -uroot db < mysql/create_report.sql
  # && mysql -uroot -proot -h localhost db < mysql/mysqldump_all_data

WORKDIR /work

ADD ./due_deligence due_deligence
ADD ./requirements.txt requirements.txt
ADD ./setup.py setup.py
ADD ./.duedeli_request_cache .duedeli_request_cache
ADD ./MANIFEST.in MANIFEST.in

# Pythonの必要なモジュールをインストール
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# パッケージ化したものをローカルにインストールする
RUN python setup.py develop

# sampleを追加
ADD sample /work/sample


CMD service mysql start \
  && cd /work \
  && /bin/bash

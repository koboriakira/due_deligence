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

# Pythonの必要なモジュールをインストール
ADD ./requirements.txt requirements.txt
RUN pip install --upgrade pip \
  && pip install -r requirements.txt


# ログ保管用のディレクトリを作成
ADD logs /work/logs

# sampleを追加
ADD sample /work/sample

# 使わないファイルたちを削除
RUN rm -fr /docker_image/*

CMD service mysql start \
  && cd /work \
  && /bin/bash

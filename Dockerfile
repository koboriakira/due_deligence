# docker build -t due_deligence_image .
FROM python:3.7.5-slim

# 必要なパッケージをインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y \
  gcc

WORKDIR /work

ADD ./due_deligence due_deligence
ADD ./requirements.txt requirements.txt
ADD ./setup.py setup.py
ADD ./MANIFEST.in MANIFEST.in

# Pythonの必要なモジュールをインストール
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# パッケージ化したものをローカルにインストールする
RUN python setup.py develop

CMD cd /work \
  && /bin/bash

# docker build -t due_deligence_image .
FROM python:3.7.5-slim

WORKDIR /docker_image

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y \
  default-mysql-server \
  default-libmysqlclient-dev \
  gcc

# mysqlの設定
ADD ./docker/mysql mysql
RUN service mysql start \
  && mysql -uroot < mysql/init.ddl \
  && mysql -uroot db < mysql/create_company.sql \
  && mysql -uroot db < mysql/create_deligence.sql \
  && mysql -uroot -proot -h localhost db < mysql/mysqldump_all_data

ADD ./requirements.txt requirements.txt
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

RUN rm -fr /docker_image/*

CMD service mysql start \
  && cd /work \
  && /bin/bash

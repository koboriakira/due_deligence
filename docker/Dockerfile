# docker build -t due_deligence_image docker
FROM python:3.7.5-slim

ADD requirements.txt tmp/requirements.txt

RUN pip install --upgrade pip && \
  pip install -r tmp/requirements.txt

CMD /bin/bash

FROM python:2.7-slim
MAINTAINER "sanadhisutandi" <sanadhis@gmail.com>

COPY requirements.txt ./
RUN mkdir -p /app
COPY start-server ./app/start-server
COPY app ./app/app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
CMD [ "bash", "start-server", "8000" ]
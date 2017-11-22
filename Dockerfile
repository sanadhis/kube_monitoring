FROM python:2.7-slim
MAINTAINER "sanadhisutandi" <sanadhis@gmail.com>

RUN apt-get update && apt-get install -y \
    gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app
COPY start-server ./app/
COPY app ./app/app

WORKDIR /app
CMD [ "bash", "start-server", "8000" ]
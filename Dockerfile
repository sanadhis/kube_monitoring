FROM python:2.7-slim
MAINTAINER "sanadhisutandi" <sanadhis@gmail.com>

COPY requirements.txt ./
COPY start-server ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash", "start-server", "8000" ]
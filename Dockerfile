# use the slimest base image possible
FROM python:2.7-slim
MAINTAINER "sanadhisutandi" <sanadhis@gmail.com>

# install gcc
RUN apt-get update && apt-get install -y \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# copy dependencies and install with pip
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

# copy app package and the start script
RUN mkdir -p /k8s
COPY app ./k8s/app
COPY start-server ./k8s/

# set working directory
WORKDIR /k8s

# Execute container using start script
CMD [ "bash", "start-server", "8000" ]
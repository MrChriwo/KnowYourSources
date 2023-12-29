# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.5-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Install Linux bash (if not present in the base image)
RUN apk add --no-cache bash

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    git \
    libffi-dev \
    openssl-dev \
    libc-dev \
    make \
    wget


RUN cd /tmp && git clone https://github.com/edenhill/librdkafka.git && \
  cd librdkafka && git checkout tags/v2.3.0 && \
  ./configure && make && make install && \
  cd ../ && rm -rf librdkafka

RUN python -m pip install -r requirements.txt

RUN apk del build-base git libffi-dev openssl-dev libc-dev make wget

EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]

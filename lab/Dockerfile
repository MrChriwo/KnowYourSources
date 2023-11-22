# Use the official Anaconda base image
FROM python:3.10-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apk --no-cache add gcc python3-dev libc-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x /app/install.sh

EXPOSE 8888

# During debugging, this entry point will be overridden.
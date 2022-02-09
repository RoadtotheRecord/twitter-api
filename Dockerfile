FROM python:3.8.7-alpine

COPY requirements.txt .

RUN apk add --no-cache build-base jpeg-dev zlib-dev &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt &&\
    apk del build-base

WORKDIR /app

ENTRYPOINT [ "python", "-B", "app.py" ]
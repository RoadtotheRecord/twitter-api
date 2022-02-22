FROM python:3.8.7-alpine

COPY requirements.txt ./

RUN apk add --no-cache --virtual .deps build-base jpeg-dev zlib-dev &&\
    python -m pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt &&\
    apk del .deps

WORKDIR /app

ENTRYPOINT [ "python", "-B", "app.py" ]
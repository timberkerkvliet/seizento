FROM python:3.10

RUN apt-get update -y && apt-get install -y \
    build-essential \
    python3-dev

COPY ./requirements.txt /

RUN pip install --no-cache -r /requirements.txt

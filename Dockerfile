FROM python:3.9-slim-buster

WORKDIR /usr/src/app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONINBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


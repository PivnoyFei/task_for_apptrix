FROM python:3.11.0-alpine

WORKDIR /srv/www/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache gcc

COPY pyproject.toml poetry.lock ./
COPY . ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install -n --no-interaction --no-ansi --no-dev
# Используйте официальный образ Python
FROM python:3.12-bullseye AS base

# Установите переменные среды
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONFAULTHANDLER 1
ENV PYTHONBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ROOT=/code
ENV TZ=Asia/Astana

# Add alpine mirrors
RUN set -eux; \
    apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    libc-dev \
    gcc \
    gettext \
    screen \
    vim \
    build-essential \
    postgresql \
    postgresql-contrib \
    netcat-traditional \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR $ROOT

# Копирование кода
COPY src $ROOT

# Обновление pip
RUN pip install --upgrade pip &&  pip install -r requirements.txt

EXPOSE 2999

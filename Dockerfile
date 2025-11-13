FROM python:3.11.5-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt update && apt install -y curl

RUN apt-get update && apt-get install -y gdal-bin libgdal-dev

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

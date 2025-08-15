FROM python:3.12.8-bullseye AS python

# RUN apt-get update && apt-get install -y gcc

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ARG BUILD=dev

WORKDIR /app

COPY ./requirements/ .

RUN pip install -q --no-cache-dir -r api.${BUILD}.txt

COPY . .

CMD ["uvicorn", "--reload", "--factory", "src.main:init"]
FROM python:3.12.8-bullseye as python

# RUN apt-get update && apt-get install -y gcc

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ARG BUILD=dev

WORKDIR /app

COPY ./requirements/api.${BUILD}.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "--reload", "src.main:app"]
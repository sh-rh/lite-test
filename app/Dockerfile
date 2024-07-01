FROM python:3.12.4-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

RUN pip install --upgrade pip
COPY reqs.txt .
RUN pip install --no-cache-dir --upgrade -r reqs.txt


COPY . ./app

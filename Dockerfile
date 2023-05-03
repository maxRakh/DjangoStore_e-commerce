FROM python:3.11-alpine3.17

WORKDIR /app

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r bazzastore1/requirements.txt


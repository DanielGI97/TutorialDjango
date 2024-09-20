FROM python:3.12.6-alpine3.20
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ../Docker/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ../../mysite/ /code/
FROM python:3.11.6-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib

RUN apt -y update \
    && apt install -y libpq-dev postgresql gcc python3-dev netcat-traditional

# set work directory
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN mkdir -p /var/log/django-app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web

WORKDIR $WORKDIR

RUN pip install --upgrade pip

COPY ./requirements.txt $WORKDIR/requirements.txt
RUN apt update && apt -y install curl inetutils-ping
RUN pip install --no-cache-dir --upgrade -r $WORKDIR/requirements.txt

RUN adduser --system --group $USER

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R $USER:$USER $APP_HOME

USER $USER

# ENTRYPOINT ["/code/entrypoint.sh"]
FROM python:3.11-slim
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt update && apt -y install curl inetutils-ping
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt
COPY . /usr/src/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
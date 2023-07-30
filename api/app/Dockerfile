FROM python:3.10-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt update && apt -y install curl inetutils-ping
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

ENTRYPOINT ["/code/entrypoint.sh"]
FROM node:16.20.1-slim

WORKDIR /code
COPY package.json /code/package.json
RUN npm install --unsafe-perm=true --allow-root
ENV PATH /code/node_modules/.bin:$PATH

COPY . /code/app/
WORKDIR /code/app/

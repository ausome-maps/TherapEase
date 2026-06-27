FROM node:22-slim

WORKDIR /code/app
COPY package.json /code/app/package.json
RUN npm install --unsafe-perm=true --allow-root
ENV PATH /code/app/node_modules/.bin:$PATH

COPY . /code/app/

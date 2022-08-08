FROM node:13

WORKDIR /app

COPY ./app/package.json .

RUN npm install --only=production

COPY ./app .

ENTRYPOINT node app.js
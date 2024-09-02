FROM node:14-alpine

WORKDIR /app

RUN apk add --no-cache curl jq

COPY . /app/

RUN npm install

RUN npm run build

EXPOSE 4000

CMD [ "npm", "start" ]

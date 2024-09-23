FROM node:21.7.3-alpine

WORKDIR /usr/src/app

COPY package.json .

RUN npm i

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
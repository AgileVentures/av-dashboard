FROM node:10 as webpack-build

RUN yarn global add npx

WORKDIR /av_dashboard

COPY package.json /av_dashboard/package.json
COPY yarn.lock /av_dashboard/yarn.lock
RUN yarn install

COPY . /av_dashboard
RUN npx webpack


RUN cat /av_dashboard/av_dashboard/static/main.js
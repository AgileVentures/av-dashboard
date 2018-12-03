FROM node:10 as webpack-builder

RUN yarn global add npx

WORKDIR /av_dashboard

COPY package.json /av_dashboard/package.json
COPY yarn.lock /av_dashboard/yarn.lock
RUN yarn install

COPY . /av_dashboard
RUN npx webpack


FROM python:3.6

ARG FLASK_ENV=dev

WORKDIR /av_dashboard

COPY . /av_dashboard/
RUN pip3 install -r requirements.txt
COPY --from=webpack-builder /av_dashboard/av_dashboard/static/ /av_dashboard/av_dashboard/static/

ENV FLASK_ENV=dev
EXPOSE 5000

CMD ["flask",  "run", "--host=0.0.0.0"]
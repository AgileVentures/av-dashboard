# build static files using webpack
FROM node:10 as webpack-builder

RUN yarn global add npx

WORKDIR /av_dashboard

COPY package.json /av_dashboard/package.json
COPY yarn.lock /av_dashboard/yarn.lock
RUN yarn install

COPY . /av_dashboard
RUN npx webpack


# build flask image with webpack output html/javascripts files
FROM python:3.6

WORKDIR /av_dashboard

COPY . /av_dashboard/
RUN pip3 install -r requirements.txt
COPY --from=webpack-builder /av_dashboard/av_dashboard/static/ /av_dashboard/av_dashboard/static/


CMD ["flask",  "run", "--host=0.0.0.0"]
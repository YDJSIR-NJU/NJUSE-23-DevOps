FROM node:14.18-stretch as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --registry=https://registry.npm.taobao.org
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

CMD nginx


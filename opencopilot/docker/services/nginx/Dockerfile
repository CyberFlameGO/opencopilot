FROM nginx:1.21.6-alpine

RUN rm /etc/nginx/nginx.conf
COPY docker/services/nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/services/nginx/api.conf /etc/nginx/conf.d/
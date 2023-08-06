FROM alpine:latest
MAINTAINER furious.luke@gmail.com

RUN mkdir -p /etc/nginx/keys && \
    apk add --update nginx && \
    rm -rf /var/cache/apk/*

ADD nginx.conf /etc/nginx/nginx.conf
ADD conf.d /etc/nginx/conf.d
ADD keys /etc/nginx/keys

EXPOSE 80 443
CMD nginx -g 'daemon off;'

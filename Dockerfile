FROM debian:8
MAINTAINER lx.nich@gmail.com

RUN apt-get update && apt-get install -y openssh-server apt-transport-https nginx

EXPOSE 22 80


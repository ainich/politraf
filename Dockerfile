FROM debian:8
MAINTAINER lx.nich@gmail.com

RUN apt-get update && apt-get install -y openssh-server apt-transport-https nginx git
RUN echo 'deb http://repo.yandex.ru/clickhouse/deb/stable/ main/' | sudo tee -a /etc/apt/sources.list
RUN  apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
RUN echo 'deb https://packagecloud.io/grafana/stable/debian/ jessie main' | sudo tee -a /etc/apt/sources.list
RUN curl https://packagecloud.io/gpg.key | sudo apt-key add -
RUN git clone git@gitlab.com:ainich/politraf.git


EXPOSE 22 80


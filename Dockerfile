FROM debian:8
MAINTAINER lx.nich@gmail.com

RUN apt-get update && apt-get install -y openssh-server apt-transport-https nginx git curl python3 python3-pip libxml2-dev libxslt1-dev python-dev python3-dev python3-lxml
RUN echo 'deb http://repo.yandex.ru/clickhouse/deb/stable/ main/' | tee -a /etc/apt/sources.list
RUN  apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
RUN echo 'deb https://packagecloud.io/grafana/stable/debian/ jessie main' | tee -a /etc/apt/sources.list
RUN curl https://packagecloud.io/gpg.key | apt-key add -
RUN mkdir -p ~/.ssh
RUN git clone https://gitlab.com/ainich/politraf.git
RUN pip3 install -r /politraf/requirements.txt
RUN python3 /politraf/install_for_docker.py

EXPOSE 22 80


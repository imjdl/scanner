# scanner
FROM ubuntu:18.04
MAINTAINER elloit
ENV LC_ALL C.UTF-8
ENV TZ=Asia/Shanghai
RUN mkdir /root/scanner
WORKDIR /root/scanner
COPY [".", "/root/scanner"]
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ["Docker/sources.list", "/etc/apt/"]
RUN apt update && apt install zmap nmap python2.7 -y
RUN python2.7 Docker/get-pip.py
RUN pip install -r requerments.txt

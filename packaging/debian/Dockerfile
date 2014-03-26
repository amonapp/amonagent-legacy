FROM ubuntu:latest
MAINTAINER Martin Rusev

RUN echo 'deb http://bg.archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list && \
    echo 'deb http://bg.archive.ubuntu.com/ubuntu precise-updates universe' >> /etc/apt/sources.list && \
    apt-get update


RUN apt-get install -y gdebi-core
ADD amon-agent_0.8_all.deb var/agent.deb

RUN gdebi -n /var/agent.deb

RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent plugins

CMD ["/bin/bash"]
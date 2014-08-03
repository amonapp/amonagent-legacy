FROM ubuntu:latest
MAINTAINER Martin Rusev

RUN echo 'deb http://bg.archive.ubuntu.com/ubuntu trusty main universe' > /etc/apt/sources.list && \
    echo 'deb http://bg.archive.ubuntu.com/ubuntu trusty-updates universe' >> /etc/apt/sources.list && \
    apt-get update


RUN apt-get install -y gdebi-core
ADD amon-agent_1.5_all.deb var/agent.deb

RUN gdebi -n /var/agent.deb

RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent test_collectors
RUN /etc/init.d/amon-agent test_plugins
RUN ls -lh /etc/amonagent/plugins

CMD ["/bin/bash"]
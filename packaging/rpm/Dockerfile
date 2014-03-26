FROM centos:latest
MAINTAINER Martin Rusev

ADD amon-agent-0.8-1.noarch.rpm var/agent.rpm

RUN yum -t -y install /var/agent.rpm

RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent plugins

CMD ["/bin/bash"]
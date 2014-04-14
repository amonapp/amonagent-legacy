FROM centos:latest
MAINTAINER Martin Rusev

ADD amon-agent-1.0.2-1.noarch.rpm var/agent.rpm

RUN yum -t -y install /var/agent.rpm

RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent test_collectors
RUN /etc/init.d/amon-agent test_plugins

CMD ["/bin/bash"]
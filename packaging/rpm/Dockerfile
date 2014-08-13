FROM martinrusev/centos:ansible
MAINTAINER Martin Rusev

ADD amon-agent-1.5.1-1.noarch.rpm var/agent.rpm

RUN yum -t -y install /var/agent.rpm


RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent test_collectors
RUN /etc/init.d/amon-agent test_plugins
RUN ls -lh /etc/amonagent/plugins


CMD ["/bin/bash"]
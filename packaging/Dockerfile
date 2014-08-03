FROM centos:latest
MAINTAINER Martin Rusev

ADD amon-agent-1.5-1.noarch.rpm var/agent.rpm


RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN wget http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
RUN rpm -Uvh remi-release-6*.rpm epel-release-6*.rpm
RUN yum -y install openssh-server openssh-clients redis


RUN yum -t -y install /var/agent.rpm



RUN /etc/init.d/amon-agent status
RUN /etc/init.d/amon-agent test_collectors
RUN /etc/init.d/amon-agent test_plugins
RUN ls -lh /etc/amonagent/plugins

RUN ls -lh rc.d/init.d
RUN /etc/init.d/amon-agent install redisdb

CMD ["/bin/bash"]
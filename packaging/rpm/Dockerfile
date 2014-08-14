FROM martinrusev/centos:ansible
MAINTAINER Martin Rusev

# ENV GIT_CURL_VERBOSE 1

ADD amon-agent-1.5.2-1.noarch.rpm var/agent.rpm

RUN yum -t -y install /var/agent.rpm

RUN /etc/init.d/amon-agent status
RUN ls -lh /etc/amonagent/plugins

RUN amonpm install boo
RUN amonpm update


CMD ["/bin/bash"]
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y gdebi-core
ADD amon-agent_2.2.1_all.deb var/agent.deb

RUN gdebi -n /var/agent.deb

RUN /etc/init.d/amon-agent status

RUN amonpm install boo
RUN amonpm update

CMD ["/bin/bash"]
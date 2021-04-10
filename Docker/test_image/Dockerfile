# Parto da un SO Debian di base
FROM raspbian/jessie
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
# UPDATE
RUN apt-get update -y 1>/dev/null
# SUDO
RUN apt-get install sudo -y 1>/dev/null
# SCRIPT
WORKDIR /
COPY setup01.sh /
RUN sudo chmod 777 setup01.sh
RUN /setup01.sh
CMD bash
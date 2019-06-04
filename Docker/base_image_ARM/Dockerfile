# Parto da un SO Debian di base
FROM arm32v7/debian:latest
ARG nome_wifi
ARG password_wifi
# QEMU
COPY qemu-arm-static /usr/bin/
# UPDATE
RUN apt-get update -y
# SUDO
RUN apt-get install sudo -y
# SCRIPT
WORKDIR /
COPY setup/01_setup.sh /
RUN /01_setup.sh $nome_wifi $password_wifi

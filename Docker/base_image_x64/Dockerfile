# Parto da un SO Debian di base
FROM debian:latest
# UPDATE
RUN apt-get update -y
# SUDO
RUN apt-get install sudo -y
# SCRIPT
WORKDIR /
COPY setup/01_setup.sh /
RUN /01_setup.sh
# GACTIONS
RUN curl https://dl.google.com/gactions/updates/bin/linux/amd64/gactions/gactions --output /usr/bin/gactions
RUN chmod +x /usr/bin/gactions
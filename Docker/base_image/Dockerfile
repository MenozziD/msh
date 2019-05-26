# Parto da un SO Debian di base
FROM debian:latest
# UPDATE
RUN apt-get update -y
# APT-UTILS
RUN apt-get install apt-utils -y
# PS, TOP, ecc..
RUN apt-get install procps -y
# NETSTAT
RUN apt-get install net-tools -y
# CURL
RUN apt-get install curl -y
# NMAP
RUN apt-get install nmap -y
# SSH
RUN apt-get install ssh -y
# WAKEONLAN
RUN apt-get install wakeonlan -y
# SAMBA per comando NET
RUN apt-get install samba-common-bin -y
# NPM
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install npm -y
# UNZIP
RUN apt-get install unzip -y
# NGROK
RUN curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip --output /usr/bin/ngrok-stable-linux-amd64.zip
RUN unzip /usr/bin/ngrok-stable-linux-amd64.zip -d /usr/bin
RUN rm /usr/bin/ngrok-stable-linux-amd64.zip
# GACTIONS
RUN curl https://dl.google.com/gactions/updates/bin/linux/amd64/gactions/gactions --output /usr/bin/gactions
RUN chmod +x /usr/bin/gactions
# PYTHON
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install --trusted-host pypi.python.org webapp3
RUN pip3 install --trusted-host pypi.python.org paste
RUN pip3 install --trusted-host pypi.python.org pexpect
RUN pip3 install --trusted-host pypi.python.org netifaces
# SQLITE
RUN apt-get install sqlite3 libsqlite3-dev -y
# SUDO
RUN apt-get install sudo -y
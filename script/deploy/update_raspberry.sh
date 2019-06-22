#!/bin/bash

sudo service msh stop
sudo mkdir msh_tmp
sudo unzip msh.zip -d msh_tmp 1>/dev/null 2>/dev/null
sudo mv msh/db .
sudo mv msh/settings.xml .
sudo rm -rf msh
sudo mv msh_tmp msh
sudo mv db msh/db
sudo mv settings.xml msh
sudo rm -rf msh/sonar-project.properties
cd msh
sudo service msh start
exit 0

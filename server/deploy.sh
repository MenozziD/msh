#!/bin/bash

sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output msh.zip
sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/deploy/update_raspberry.sh --output update_raspberry.sh 1>/dev/null
sudo chmod 744 update_raspberry.sh
sudo unzip msh.zip 1>/dev/null
sudo mv msh-master/server/msh msh_tmp 1>/dev/null
sudo rm -rf msh-master 1>/dev/null
sudo rm -rf msh.zip 1>/dev/null
cd msh_tmp
sudo zip -r  ../msh.zip * 1>/dev/null
cd ..
sudo rm -rf msh_tmp  1>/dev/null
sudo ./update_raspberry.sh
sudo rm -rf update_raspberry.sh msh.zip
exit 0

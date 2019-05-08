sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install webapp3
sudo pip3 install paste
sudo pip3 install pexpect
sudo apt-get install sqlite3 libsqlite3-dev
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
tar -xvzf msh.tar.gz
cd msh
mkdir db
sudo sqlite3 ./db/system.db
sqlite3 ./db/system.db < ./script/create.sql
python3 msh.py
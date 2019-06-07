#!/bin/bash

pgrep python | awk '{print $0}' | xargs sudo kill -9
mkdir msh_tmp
unzip msh.zip -d msh_tmp 1>/dev/null 2>/dev/null
mv msh/db .
mv msh/settings.xml .
rm -rf msh
mv msh_tmp msh
rm -rf msh/script
mv db msh/db
mv settings.xml msh
cd msh
sudo python3 msh.py 1>/dev/null 2>/dev/null &
exit 0

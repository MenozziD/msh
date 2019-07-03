#!/bin/bash

cd msh
sudo useradd test_user
echo 'test_user:test_password' | sudo chpasswd
sudo sqlite3 ./db/test.db < create.sql
sudo python3 -m coverage erase
sudo python3 -m coverage run --rcfile=setup.cfg -m pytest --junitxml=test-report.xml
sudo mv .coverage ..
sudo mv test-report.xml ..
sudo rm db/test.db
sudo userdel test_user
cd ..
exit 0

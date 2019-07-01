#!/bin/bash

cd msh
sudo adduser test_user
echo test_password | passwd test_user --stdin
sudo sqlite3 ./db/test.db < create.sql
sudo python3 -m coverage erase
sudo python3 -m coverage run -m pytest --junitxml=test-report.xml
sudo mv .coverage ..
sudo mv test-report.xml ..
sudo rm db/test.db
sudo userdel test_user
cd ..
exit 0

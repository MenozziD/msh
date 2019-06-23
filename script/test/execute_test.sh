#!/bin/bash

cd msh
sudo python3 -m coverage erase
sudo python3 -m coverage run -m pytest --junitxml=test-report.xml
sudo mv .coverage ..
sudo mv test-report.xml ..
cd ..
exit 0
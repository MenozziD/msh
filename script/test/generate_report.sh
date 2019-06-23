#!/bin/bash

sudo mv .coverage msh
sudo mv test-report.xml msh
cd msh
sudo python3 -m coverage xml -i
cd ..
exit 0
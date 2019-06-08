#!/bin/bash

sudo dd if=/dev/zero of=/root/swapfile1 bs=1M count=2048
sudo chmod 600 /root/swapfile1
sudo mkswap /root/swapfile1
sudo swapon /root/swapfile1
sudo cat /etc/fstab
swapon -s
free -k
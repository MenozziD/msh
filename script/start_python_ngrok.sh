#!/bin/bash

ngrok start --config=../server/ngrok/ngrok.yaml --all 1> /dev/null 2> /dev/null &
cd ../server/msh/
python3 msh.py 
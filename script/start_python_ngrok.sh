#!/bin/bash

ngrok start --config=../server/ngrok.yaml --all 1> /dev/null 2> /dev/null &
python3 ../server/msh/msh.py 
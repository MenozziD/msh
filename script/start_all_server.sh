#!/bin/bash

cd ../server/fake-oauth-server-nodejs
npm start 1> /dev/null 2> /dev/null &
ngrok start --config=../ngrok/ngrok.yaml --all 1> /dev/null 2> /dev/null &
cd ../msh
python3 msh.py
#!/bin/bash

cd fake-oauth-server-nodejs
npm start 1> /dev/null 2> /dev/null &
ngrok start --config=../ngrok/ngrok.yaml --all 1> /dev/null 2> /dev/null &
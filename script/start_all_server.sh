#!/bin/bash

cd ../server/oauth
npm start 1> /dev/null 2> /dev/null &
cd ../msh
python3 msh.py 1> /dev/null 2> /dev/null &
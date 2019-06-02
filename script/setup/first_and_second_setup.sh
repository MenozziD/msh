#!/bin/bash

if [ "$#" -ne 7 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME_WEBAPP PASSWORD_WEBAPP DOMINIO_OAUTH DOMINIO_WEBAPP NOME_WIFI PASSWORD_WIFI" >&2
  exit 1
fi

./01_setup.sh
./02_setup.sh $1 $2 $3 $4 $5 $6 $7
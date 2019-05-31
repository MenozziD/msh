#Accesso alla cartella
cd /c/Users/Simone.simone/Documents/Repository/msh/Docker/raspberry_image

#Deploy container
./deploy.sh test-rasp-18a53 sgarzo cronaldo7 oauthsga casasga 

# kill processo ngrok
ps -aux | grep ngrok | grep yaml | awk '{print $2}' | xargs kill -9

# start dns serveo
ssh -o "StrictHostKeyChecking no" -R casamenoz:80:localhost:65177 -R oauthmenoz:80:localhost:3000 serveo.net

# Esecuzione di un'immagine arm con qemu (funziona solo su macchina linux)
docker run -v /usr/bin/qemu-arm-static:/usr/bin/qemu-arm-static --rm -ti arm32v7/debian:stretch-slim

# Accedere al container
docker exec -i -t raspberrypi /bin/bash
docker exec -i -t esprele /bin/bash

#Creare export file system del container
docker export raspberrypi > msh_so.tar

# Info sulla VM di Docker in utilizzo
docker version

# Info sullo stato di Docker
docker info

# Rimuove tutte le immagini
docker image ls | awk '{print $3}' | xargs docker image rm

# Rimuove tutti i container
docker container ls --all | awk '{print $1}' | xargs docker container rm

# Creazione di un'immagine
docker build . --tag=msh:v0.0.1

# Creazione di un'immagine ed esecuzione
docker build . --build-arg ngrok_auth_token='TOKEN' --build-arg google_actions_project_id='ID_PROJECT' --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1

# Stoppare/Avviare il container
docker container stop raspberrypi
docker container run raspberrypi
docker inspect raspberrypi

# Mostra le reti che possono usare i container
docker netwrok ls

# Mostra chi fa parte della rete
docker netwrok inspect bridge

# Operazioni sulle macchine che runnano Docker
docker-machine ls
docker-machine ip
docker-machine stop default
docker-machine start default
docker-machine create --driver=qemu --qemu-program=qemu-system-arm qemu-test
docker-machine rm qemu-test
docker-machine ssh default

# Download di una libreria GO
go get github.com/docker/machine/libmachine/drivers/plugin

#Build di un progetto GO
go build -i -o docker-machine-driver-qemu.exe

#Creo la action su google action a partire dal json
gactions --verbose update --action_package ./msh/action.json --project smart-home-android-thing-deadd

#Guardo lo stato della google action
.\gactions --verbose get --project test-rasp-18a53 --version draft

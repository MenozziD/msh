# Execute webapp in background
sudo python3 msh.py 1>/dev/null 2>/dev/null &

# Kill della webapp
pgrep python | awk '{print $0}' | xargs sudo kill -9

# Copiare directory su raspberry con ssh
scp -r server pi@192.168.1.106:/home/pi

# Copiare un file su raspberry con ssh
scp 02_setup.sh pi@192.168.1.106:/home/pi/02_setup.sh

# SQLITE 3 cli view
.mode column
.header on

# Lista board
sudo arduino-cli board listall

# Compilazione per ESP
sudo arduino-cli compile --fqbn esp8266:esp8266:generic test

# Ricavare USB utilizzata da dispositivo
usb=`arduino-cli board list | grep tty | awk '{print $1}'`

#Printare tutto tranne ultima colonna
arduino-cli board listall | awk '{$NF=""; print $0}'

#Printare core del dispositivo
sudo arduino-cli board listall | grep "ESPresso Lite 1.0" | awk '{print $NF}'

# Upload su ESP
sudo arduino-cli upload -p $usb --fqbn esp8266:esp8266:generic test

#Deploy container
./deploy.sh project-id sga cr7 oauthsga casasga

#Kill processo ngrok
ps -aux | grep ngrok | grep yaml | awk '{print $2}' | xargs kill -9

#Start dns serveo
ssh -o "StrictHostKeyChecking no" -R casamenoz:80:localhost:65177 -R oauthmenoz:80:localhost:3000 serveo.net

# Accedere al container
docker exec -i -t raspberry-x64 /bin/bash
docker exec -i -t raspberry-arm /bin/bash
docker exec -i -t esprele /bin/bash

#Creare export file system del container
docker export raspberry-arm > raspberry_arm.tar
# Make tar
tar -cvf name.tar /path/to/directory

#Convertire tar to img
dd if=raspberry_arm.tar of=1.img

# Rimuove tutte le immagini
docker image ls | awk '{print $3}' | xargs docker image rm

# Rimuove tutti i container
docker container ls --all | awk '{print $1}' | xargs docker container rm

# Creazione di un'immagine
docker build . --tag=msh:v0.0.1

# Esecuzione di un'immagine arm con qemu (funziona solo su macchina linux)
docker run -v /usr/bin/qemu-arm:/usr/bin/qemu-arm --rm -ti arm32v7/debian:latest

# Creazione di un'immagine ed esecuzione
docker build . --build-arg ngrok_auth_token='TOKEN' --build-arg google_actions_project_id='ID_PROJECT' --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1

# Stoppare/Avviare il container
docker container stop raspberry-x64
docker container stop raspberry-arm
docker container run raspberry-x64
docker inspect raspberry-x64

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

# Info sulla VM di Docker in utilizzo
docker version

# Info sullo stato di Docker
docker info

# Download di una libreria GO
go get github.com/docker/machine/libmachine/drivers/plugin

#Build di un progetto GO
go build -i -o docker-machine-driver-qemu.exe

#Creo la action su google action a partire dal json
gactions --verbose update --action_package ./msh/action.json --project smart-home-android-thing-deadd

#Guardo lo stato della google action
gactions --verbose get --project test-rasp-18a53 --version draft

# MSH

Hub per comunicare con dispositivi tramite Wi-Fi

## Preparazione

Di seguito i passi per effettuare la configurazione del dispositivo

### Prerequisiti

1. Raspberry Pi 3
2. Connessione Wi-Fi
3. [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

### Installazzione

Effettuare l'installazione di python3

```bash
sudo apt-get update
sudo apt-get install python3
```

Installare le librerie necessarie di python3

```bash
sudo pip3 install webapp3
sudo pip3 install paste
sudo pip3 install pexpect
```

Installare SQL Lite
```bash
sudo apt-get update
sudo apt-get install sqlite3 libsqlite3-dev
```

Effettuare il download dello zip da GitHub

```bash
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
```

Eseguire la decompressione dell'archivio appena scaricato

```bash
tar -xvzf msh.tar.gz
```

Entrare nella directoy generata al passo precedente

```bash
cd msh
```

Creare ed accedere alla cartella per il Database

```bash
mkdir db
cd db
```

Creare il Database

```bash
sqlite3 database.db
```

Creare lo schema del Database

```bash
sqlite3 database.db < ../script/create.sql
```

Avviare il server

```bash
cd ..
python3 msh.py
```

## Utilizzo

Accedere con Chrome al seguente indirizzo

```
http://localhost:8080
```

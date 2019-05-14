# MSH

Hub per comunicare con dispositivi tramite Wi-Fi

## Preparazione

Di seguito i passi per effettuare la configurazione del dispositivo

### Prerequisiti

1. Raspberry Pi 3
2. Connessione Wi-Fi
3. [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

### Installazzione

Effettuare il download dello zip da GitHub

```bash
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
```

Eseguire la decompressione dell'archivio appena scaricato

```bash
tar -xvzf msh.tar.gz
```

Entrare nella directoy setup all'interno della cartella generata al passo precedente

```bash
cd msh/setup
```

Eseguire il seguente comando

```bash
./setup.sh
```


## Utilizzo attraverso container Docker

Con i seguenti passaggi si può eseguire l'installazione in un container Docker

### Prerequisiti

1. Avere [Docker Toolbox](https://download.docker.com/win/stable/DockerToolbox.exe) installato sulla macchina 

### Preparazione

Effettuare il download dello zip da GitHub

```bash
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
```

Eseguire la decompressione dell'archivio appena scaricato

```bash
tar -xvzf msh.tar.gz
```

Accedere alla directory base_image dentro alla cartella Docker contenuta all'interno della cartella ottenuta al passo precedente

```bash
cd msh/Docker/base_image
```

Effettuare una build Docker

```bash
docker build . --tag=msh:v0.0.1
```

Verificare che l'immagine sia stata creata

```bash
docker image ls
```

Copiare la cartella msh dentro alla cartella target_image
```bash
cp ../../msh ../target_image
```

Accedere alla cartella target_image
```bash
cd ../target_image
```

Effettuare una build Docker

```bash
docker build . --tag=msrheal:v0.0.1
```

Verificare che l'immagine sia stata creata

```bash
docker image ls
```

Lanciare un container Docker con l'immagine appena creata

```bash
docker run -d --name raspberrypi -p 8080:65177 msrheal:v0.0.1
```

Verificare che il container sia in esecuzione

```bash
docker container ls
```

Aprire VirtualBox accedere alle impostazione della macchina default -> Rete -> Scheda 1 -> Avanzate -> Inoltro delle porte e impostare la seguente regola
```bash
Protocollo  IP dell'host  Porta dell'host  IP del guest  Porta del guest
TCP                       80                             8080
```

Accedere con Chrome al seguente indirizzo

```
http://localhost
```

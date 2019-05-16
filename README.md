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

Entrare nella directoy setup all'interno della cartella generata al passo precedente

```bash
cd msh/setup
```

Eseguire il seguente comando

```bash
./setupDocker.sh
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

### Deploy successivi

Se a segutio di modifiche al sorgente si vuole effettuare un nuovo deploy eseguire i seguenti comandi

```
cd msh/Docker/raspberry_image
./deploy.sh
```

### Avviare altri nodi

Se si desidera creare una rete di nodi con cui comunicare tramite il container del raspberry

```
cd msh/Docker/esp_rele_image
./deploy.sh
```

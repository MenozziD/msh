# MSH

Hub per comunicare con dispositivi tramite Wi-Fi

## Preparazione

Di seguito i passi per effettuare la configurazione del dispositivo

### Prerequisiti

1. Raspberry Pi 3
2. Connessione Wi-Fi
3. [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
4. Avere un account google

### Installazzione

Effettuare il download dello zip da GitHub

```bash
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
```

Eseguire la decompressione dell'archivio appena scaricato

```bash
tar -xvzf msh.tar.gz
```

Entrare nella directoy script all'interno della cartella generata al passo precedente

```bash
cd msh/script
```

Registrarsi su [Ngrok](https://ngrok.com/) con l'account google e recuperare il Tunnel Authtoken dalla scheda Auth

Creare un'progetto su [Google Actions](https://console.actions.google.com/) dargli un nome e scegliere Italia

Andare nella sezione Project Settings attraverso l'ingranaggio di fianco ad Overview e copiare il campo Project ID

Eseguire il seguente comando

```bash
./setup.sh <NGROK_AUTHTOKEN> <GOOGLE_PROJECT_ID>
```

Eseguire il seguente comando ed effettuare le operazioni richieste

```bash
gactions update --action_package ./msh/action.json --project <GOOGLE_PROJECT_ID>
```

Eseguire il seguente comando 

```bash
./start.sh
```

Vedere i log di MSH

```bash
cat msh.log
```

Accedere alla sezione Account linking all'interno del progetto su Google Actions

1. Account creation: No, I only want to allow account creation on my website
2. Linking type: OAuth Authorization Code
3. Client information - Client ID: `RKkWfsi0Z9`
4. Client information - Client secret: `eToBzeBT7OwrPQO8mZHsZtLp1qhQbe`
5. Client information - Authorization URL: copiare l'endpoint URL oauth contenuto nei log
6. Client information - Token URL: copiare l'endpoint URL token contenuto nei log
7. Testing instructions: test

Premere Save e poi Test

Accedere all'endpoint URL webapp contenuto nei log

A questo punto si può aggiungere il dispositivo all'interno di Google Home

## Utilizzo attraverso container Docker

Con i seguenti passaggi si può eseguire l'installazione in un container Docker

### Prerequisiti

1. Avere [Docker Toolbox](https://download.docker.com/win/stable/DockerToolbox.exe) installato sulla macchina 
2. Connessione Wi-Fi
3. Avere un account google

### Preparazione

Effettuare il download dello zip da GitHub

```bash
curl -o msh.tar.gz https://github.com/VanMenoz92/msh/archive/master.zip
```

Eseguire la decompressione dell'archivio appena scaricato

```bash
tar -xvzf msh.tar.gz
```

Entrare nella directoy script all'interno della cartella generata al passo precedente

```bash
cd msh/script
```

Registrarsi su [Ngrok](https://ngrok.com/) con l'account google e recuperare il Tunnel Authtoken dalla scheda Auth

Creare un'progetto su [Google Actions](https://console.actions.google.com/) dargli un nome e scegliere Italia

Andare nella sezione Project Settings attraverso l'ingranaggio di fianco ad Overview e copiare il campo Project ID

Eseguire il seguente comando

```bash
./setupDocker.sh <NGROK_TOKEN> <GOOGLE_PROJECT_ID>
```

Verificare che il container sia in esecuzione

```bash
docker container ls
```

Accedere al container

```bash
docker exec -i -t raspberrypi /bin/bash
```

Eseguire il seguente comando ed effettuare le operazioni richieste

```bash
gactions update --action_package ./msh/action.json --project <GOOGLE_PROJECT_ID>
```

Vedere i log di MSH

```bash
cat msh/msh.log
```

Accedere alla sezione Account linking all'interno del progetto su Google Actions

1. Account creation: No, I only want to allow account creation on my website
2. Linking type: OAuth Authorization Code
3. Client information - Client ID: `RKkWfsi0Z9`
4. Client information - Client secret: `eToBzeBT7OwrPQO8mZHsZtLp1qhQbe`
5. Client information - Authorization URL: copiare l'endpoint URL oauth contenuto nei log
6. Client information - Token URL: copiare l'endpoint URL token contenuto nei log
7. Testing instructions: test

Premere Save e poi Test

Accedere all'endpoint URL webapp contenuto nei log

A questo punto si può aggiungere il dispositivo all'interno di Google Home

### Deploy successivi

Se a segutio di modifiche al sorgente si vuole effettuare un nuovo deploy eseguire i seguenti comandi

```
cd msh/Docker/raspberry_image
./deploy.sh <NGROK_TOKEN> <GOOGLE_PROJECT_ID>
```

Accedere al container

```bash
docker exec -i -t raspberrypi /bin/bash
```

Eseguire il seguente comando ed effettuare le operazioni richieste

```bash
gactions update --action_package ./msh/action.json --project <GOOGLE_PROJECT_ID>
```

Vedere i log di MSH

```bash
cat msh/msh.log
```

Accedere alla sezione Account linking all'interno del progetto su Google Actions

1. Account creation: No, I only want to allow account creation on my website
2. Linking type: OAuth Authorization Code
3. Client information - Client ID: `RKkWfsi0Z9`
4. Client information - Client secret: `eToBzeBT7OwrPQO8mZHsZtLp1qhQbe`
5. Client information - Authorization URL: copiare l'endpoint URL oauth contenuto nei log
6. Client information - Token URL: copiare l'endpoint URL token contenuto nei log
7. Testing instructions: test

Premere Save e poi Test

Accedere all'endpoint URL webapp contenuto nei log

A questo punto si può aggiungere il dispositivo all'interno di Google Home

### Avviare altri nodi

Se si desidera creare una rete di nodi con cui comunicare tramite il container del raspberry

```
cd msh/Docker/esp_rele_image
./deploy.sh
```

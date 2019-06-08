from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from module import XmlReader
from datetime import datetime
from subprocess import PIPE, run, check_output
from urllib import request


class UploadArduino(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
                data = loads(body)
                tipo_operazione = data['tipo_operazione']
                core = data['core']
                tipologia = data['tipologia']
                if tipo_operazione == "upload":
                    cmd = "arduino-cli board list | grep tty | awk '{print $1}'"
                    cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                    if cmd_out != "":
                        run(["mkdir", tipologia])
                        run(["curl", "https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/" + tipologia + "/" + tipologia + ".ino", "--output", tipologia + "/" + tipologia + ".ino"])
                        run(["curl", "https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/" + tipologia + "/index.h", "--output", tipologia + "/" + "index.h"])
                        cmd = "arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'"
                        core = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                        cmd = run(["sudo", "arduino-cli", "upload", "-p", cmd_out, "--fqbn", core, tipologia], stdout=PIPE, stderr=PIPE)
                        cmd_out = str(cmd.stdout)[2:-1].replace("\\n", "\n")
                        cmd_err = str(cmd.stderr)[2:-1].replace("\\n", "\n")
                        run(["sudo", "rm", "-rf", tipologia])
                        if cmd_err == "":
                            # fare parsing sull output per creare la response con le info della compilazione
                            response['cmd_output'] = cmd_out
                            response['output'] = 'OK'
                        else:
                            response['output'] = cmd_err
                    else:
                        response['output'] = 'Nessun dispositivo collegato'
                if tipo_operazione == "core":
                    cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
                    cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                    cores = []
                    for core in cmd_out.split("\n")[1:]:
                        if core != '':
                            cores.append(core[:-1])
                    response['cores'] = cores
                    response['output'] = 'OK'
                if tipo_operazione == "tipo":
                    url = "https://api.github.com/repos/VanMenoz92/msh/contents/devices?ref=master"
                    res = loads(request.urlopen(url).read().decode('utf-8'))
                    types = []
                    for device in res:
                        types.append(device['name'])
                    response['types'] = types
                    response['output'] = 'OK'
            else:
                response['output'] = 'Devi effettuare la login per utilizzare questa API'
                if self.session.get('role') == 'USER':
                    response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            info("RESPONSE CODE: %s", self.response.status)
            info("RESPONSE PAYLOAD: %s", response)

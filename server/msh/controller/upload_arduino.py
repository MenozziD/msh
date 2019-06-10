from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from module import XmlReader
from datetime import datetime
from subprocess import check_output
from module import compile_and_upload
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
                    response['result_command'] = compile_and_upload(core, tipologia, make_upload=True, remove_dir=True)
                    response['output'] = 'OK'
                if tipo_operazione == "core":
                    cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
                    info("Eseguo il comando: %s", cmd)
                    cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                    cores = []
                    for core in cmd_out.split("\n")[1:]:
                        if core != '':
                            cores.append(core[:-1])
                    response['cores'] = cores
                    response['output'] = 'OK'
                if tipo_operazione == "tipo":
                    url = "https://api.github.com/repos/VanMenoz92/msh/contents/devices?ref=master"
                    info("MAKE REQUEST: %s", url)
                    res = loads(request.urlopen(url).read().decode('utf-8'))
                    info("RESPONSE: %s", res)
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

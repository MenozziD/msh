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
            response = UploadArduino.check_user(self.session.get('user'), self.session.get('role'))
            if response['output'] == 'OK':
                data = loads(body)
                tipo_operazione = data['tipo_operazione']
                core = data['core']
                tipologia = data['tipologia']
                funzioni = {
                    'upload': UploadArduino.upload_code,
                    'core': UploadArduino.core_list,
                    'tipo': UploadArduino.tipo_list
                }
                parametri = {
                    'upload': [core, tipologia],
                    'core': [],
                    'tipo': []
                }
                response = funzioni[tipo_operazione](*parametri[tipo_operazione])
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

    @staticmethod
    def check_user(user, role):
        response = {}
        if user is not None and role == 'ADMIN':
            response['output'] = 'OK'
        else:
            response['output'] = 'Devi effettuare la login per utilizzare questa API'
            if role == 'USER':
                response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
        return response

    @staticmethod
    def upload_code(core, tipologia):
        response = {
            'result_command': compile_and_upload(core, tipologia, make_upload=True, remove_dir=True),
            'output': 'OK'
        }
        return response

    @staticmethod
    def core_list():
        cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
        info("Eseguo il comando: %s", cmd)
        cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
        cores = []
        for core in cmd_out.split("\n")[1:]:
            if core != '':
                cores.append(core[:-1])
        response = {
            'cores': cores,
            'output': 'OK'
        }
        return response

    @staticmethod
    def tipo_list():
        url = "https://api.github.com/repos/VanMenoz92/msh/contents/devices?ref=master"
        info("MAKE REQUEST: %s", url)
        res = loads(request.urlopen(url).read().decode('utf-8'))
        info("RESPONSE: %s", res)
        types = []
        for device in res:
            types.append(device['name'])
        response = {
            'types': types,
            'output': 'OK'
        }
        return response

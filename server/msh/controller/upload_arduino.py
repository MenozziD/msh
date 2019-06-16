from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from module import XmlReader, compile_and_upload
from datetime import datetime
from subprocess import check_output
from urllib import request


class UploadArduino(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            response = UploadArduino.check(self.session.get('user'), self.session.get('role'), body)
            if response['output'] == 'OK':
                data = loads(body)
                tipo_operazione = data['tipo_operazione']
                core = ''
                tipologia = ''
                if 'core' in data:
                    core = data['core']
                if 'tipologia' in data:
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
    def check(user, role, body):
        response = {}
        if body != "" and UploadArduino.validate_format(body):
            data = loads(body)
            if 'tipo_operazione' in data and data['tipo_operazione'] in ('upload', 'core', 'tipo'):
                response = UploadArduino.check_user(user, role, data['tipo_operazione'])
                if response['output'] == 'OK':
                    if data['tipo_operazione'] == 'upload':
                        response = UploadArduino.check_core(data)
                        if response['output'] == 'OK':
                            response = UploadArduino.check_tipologia(data)
            else:
                if 'tipo_operazione' in data:
                    response[
                        'output'] = 'Il campo tipo_operazione deve assumere uno dei seguenti valori: upload, core, tipo'
                else:
                    response['output'] = 'Il campo tipo_operazione è obbligatorio'
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in 'upload':
                if role != 'ADMIN':
                    response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
                else:
                    response['output'] = 'OK'
            else:
                response['output'] = 'OK'
        else:
            response['output'] = 'Devi effettuare la login per utilizzare questa API'
        return response

    @staticmethod
    def check_core(data):
        response = {}
        cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
        info("Eseguo il comando: %s", cmd)
        cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
        core_list = []
        for core in cmd_out.split("\n")[1:]:
            if core != '':
                core_list.append(core[:-1])
        if 'core' in data and data['core'] in core_list:
            response['output'] = 'OK'
        else:
            if 'core' in data:
                response['output'] = "Il campo core deve assumere uno dei seguenti valori: " + ', '.join(core_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo core"
        return response

    @staticmethod
    def check_tipologia(data):
        response = {}
        url = "https://api.github.com/repos/VanMenoz92/msh/contents/devices?ref=master"
        info("MAKE REQUEST: %s", url)
        res = loads(request.urlopen(url).read().decode('utf-8'))
        info("RESPONSE: %s", res)
        tipologia_list = []
        for device in res:
            tipologia_list.append(device['name'])
        if 'tipologia' in data and data['tipologia'] in tipologia_list:
            response['output'] = 'OK'
        else:
            if 'tipologia' in data:
                response['output'] = "Il campo tipologia deve assumere uno dei seguenti valori: " + ', '.join(tipologia_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo tipologia"
        return response

    @staticmethod
    def validate_format(body):
        try:
            loads(body)
        except ValueError:
            return False
        return True

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

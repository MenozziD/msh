from controller import BaseHandler
from logging import info, exception
from json import loads
from module import compile_arduino, upload_arduino, execute_os_cmd, set_api_response, validate_format, execute_request_http


class UploadArduino(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            response = UploadArduino.check(self.session.get('user'), self.session.get('role'), self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                tipo_operazione = data['tipo_operazione']
                core = ''
                tipologia = ''
                if 'core' in data:
                    core = data['core']
                if 'tipologia' in data:
                    tipologia = data['tipologia']
                funzioni = {
                    'upload': UploadArduino.upload_code,
                    'compile': UploadArduino.compile_code,
                    'core': UploadArduino.core_list,
                    'tipo': UploadArduino.tipo_list
                }
                parametri = {
                    'upload': [core, tipologia],
                    'compile': [core, tipologia],
                    'core': [],
                    'tipo': []
                }
                response = funzioni[tipo_operazione](*parametri[tipo_operazione])
            else:
                raise Exception(response['output'])
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            set_api_response(response, self.response)

    @staticmethod
    def check(user, role, requestt, body):
        response = {}
        if body != "" and validate_format(requestt):
            data = requestt.json
            if 'tipo_operazione' in data and data['tipo_operazione'] in ('upload', 'core', 'tipo', 'compile'):
                response = UploadArduino.check_user(user, role, data['tipo_operazione'])
                response = UploadArduino.check_upload_compile(response, data)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = 'Il campo tipo_operazione deve assumere uno dei seguenti valori: upload, compile, core, tipo'
                else:
                    response['output'] = 'Il campo tipo_operazione è obbligatorio'
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
        return response

    @staticmethod
    def check_upload_compile(response, data):
        if response['output'] == 'OK' and data['tipo_operazione'] in ('upload', 'compile'):
            response = UploadArduino.check_core(data)
            if response['output'] == 'OK':
                response = UploadArduino.check_tipologia(data)
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('upload', 'compile'):
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
        cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
        response = execute_os_cmd(cmd, check_out=True)
        core_list = []
        for core in response['cmd_out'].split("\n")[1:]:
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
        res = loads(execute_request_http(url))
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
    def upload_code(core, tipologia):
        return upload_arduino(core, tipologia)

    @staticmethod
    def compile_code(core, tipologia):
        return compile_arduino(core, tipologia)

    @staticmethod
    def core_list():
        cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
        response = execute_os_cmd(cmd, check_out=True)
        cores = []
        for core in response['cmd_out'].split("\n")[1:]:
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
        res = loads(execute_request_http(url))
        types = []
        for device in res:
            types.append(device['name'])
        response = {
            'types': types,
            'output': 'OK'
        }
        return response

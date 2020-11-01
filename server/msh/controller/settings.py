from controller import BaseHandler
from logging import info, exception
from module import XmlReader, delete_user, update_user, set_api_response, validate_format, get_string, wifi_ap_info, traverse
from copy import deepcopy


class Settings(BaseHandler):

    tipo_operazione = ['list', 'update']

    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            response = Settings.check(self.session.get('user'), self.session.get('role'), self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                tipo_operazione = data['tipo_operazione']
                settings = None
                if 'settings' in data:
                    settings = data['settings']
                funzioni = {
                    'list': Settings.settings_list,
                    'update': Settings.settings_update,
                }
                parametri = {
                    'list': [],
                    'update': [settings]
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
    def check(user, role, request, body):
        response = {}
        if body != "" and validate_format(request):
            data = request.json
            if 'tipo_operazione' in data and data['tipo_operazione'] in Settings.tipo_operazione:
                response = Settings.check_user(user, role)
                response = Settings.check_operation_param(response, data)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = get_string(24, da_sostituire="tipo_operazione", da_aggiungere=', '.join(Settings.tipo_operazione))
                else:
                    response['output'] = get_string(23, da_sostituire="tipo_operazione")
        else:
            if body != "":
                response['output'] = get_string(22)
            else:
                response['output'] = get_string(21)
        return response

    @staticmethod
    def check_user(user, role):
        response = {}
        if user is not None:
            if role != 'ADMIN':
                response['output'] = get_string(26)
            else:
                response['output'] = 'OK'
        else:
            response['output'] = get_string(25)
        return response

    @staticmethod
    def check_operation_param(response, data):
        if response['output'] == 'OK':
            if data['tipo_operazione'] == 'update':
                response = Settings.check_update(data)
        return response

    @staticmethod
    def check_update(data):
        response = {}
        if 'settings' in data:
            response['output'] = 'OK'
        else:
            response['output'] = get_string(23, da_sostituire="settings")
        return response

    @staticmethod
    def settings_list():
        settings = deepcopy(XmlReader.settings)
        info(XmlReader.settings)
        del settings['ambiente']
        del settings['log']
        del settings['path_db']
        del settings['path_datastore']
        del settings['protocol']
        del settings['timestamp']
        del settings['wifi_default']
        for (key, value) in settings['dns'].items():
            del settings['dns'][key]['test_url']
            del settings['dns'][key]['domain']
        response = {
            'output': 'OK',
            'settings': settings
        }
        return response

    @staticmethod
    def settings_update(new_settings):
        f = open("settings.xml", "r")
        data = f.read()
        f.close()
        for path, node in traverse(new_settings):
            if isinstance(node, str):
                now = ""
                for p in path:
                    if now == "":
                        now = XmlReader.settings[p]
                    else:
                        now = now[p]
                data = data.replace(path[len(path)-1] + ">" + now + "<", path[len(path)-1] + ">" + node + "<")
        f = open("settings.xml", "w")
        f.write(data)
        f.close()
        protocol = XmlReader.settings['protocol']
        XmlReader("settings.xml")
        XmlReader.settings['protocol'] = protocol
        response = {
            'output': 'OK'
        }
        return response

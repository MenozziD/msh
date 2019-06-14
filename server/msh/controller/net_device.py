from controller import BaseHandler
from logging import info, exception
from module import DbManager
from module import XmlReader
from json import dumps, loads
from datetime import datetime


class NetDevice(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            data = loads(body)
            DbManager()
            response = NetDevice.check(self.session.get('user'), self.session.get('role'), data)
            if response['output'] == 'OK':
                type_op = data['tipo_operazione']
                tipo = ''
                mac = ''
                codice = ''
                user = ''
                password = ''
                if 'codice' in data:
                    codice = data['codice']
                if 'tipo' in data:
                    tipo = data['tipo']
                if 'mac' in data:
                    mac = data['mac']
                if 'user' in data:
                    user = data['user']
                if 'password' in data:
                    password = data['password']
                if response['output'] == 'OK':
                    funzioni = {
                        'list': NetDevice.device_list,
                        'type': NetDevice.device_type,
                        'command': NetDevice.device_command,
                        'update': NetDevice.device_update,
                        'delete': NetDevice.device_delete,
                    }
                    parametri = {
                        'list': [self.session.get('role')],
                        'type': [],
                        'command': [tipo],
                        'update': [mac, codice, tipo, user, password],
                        'delete': [mac]
                    }
                    response = funzioni[type_op](*parametri[type_op])
            DbManager.close_db()
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
    def check(user, role, data):
        response = {}
        if 'tipo_operazione' in data and data['tipo_operazione'] in ('list', 'type', 'command', 'update', 'delete'):
            response = NetDevice.check_user(user, role, data['tipo_operazione'])
            if response['output'] == 'OK':
                if data['tipo_operazione'] == 'command':
                    response = NetDevice.check_tipo(data, required=True)
                if data['tipo_operazione'] == 'delete':
                    response = NetDevice.check_mac(data)
                if data['tipo_operazione'] == 'update':
                    response = NetDevice.check_mac(data)
                    if response['output'] == 'OK':
                        response = NetDevice.check_tipo(data)
                        if response['output'] == 'OK':
                            response = NetDevice.check_code(data)
        else:
            if 'tipo_operazione' in data:
                response['output'] = 'Il campo tipo_operazione deve assumere uno dei seguenti valori: list, type, command, update, delete'
            else:
                response['output'] = 'Il campo tipo_operazione è obbligatorio'
        return response

    @staticmethod
    def check_tipo(data, required=False):
        response = {}
        type_list = [d['type_code'] for d in DbManager.select_tb_net_device_type()]
        if 'tipo' in data and data['tipo'] in type_list:
            response['output'] = 'OK'
        else:
            if 'tipo' in data:
                response['output'] = "Il campo tipo deve assumere uno dei seguenti valori: " + ', '.join(type_list)
            else:
                if required:
                    response['output'] = "Per l'operazione scelta è obbligatorio il campo tipo"
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def check_mac(data):
        response = {}
        mac_list = [d['net_mac'] for d in DbManager.select_tb_net_device()]
        if 'mac' in data and data['mac'] in mac_list:
            response['output'] = 'OK'
        else:
            if 'mac' in data:
                response['output'] = "Il campo mac deve assumere uno dei seguenti valori: " + ', '.join(mac_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo mac"
        return response

    @staticmethod
    def check_code(data):
        response = {}
        trovato = False
        devices = DbManager.select_tb_net_device()
        to_update = DbManager.select_tb_net_device(data['mac'])[0]
        response['output'] = "OK"
        if 'codice' in data:
            if data['codice'] != to_update['net_code']:
                for device in devices:
                    if device['net_code'] == data['codice']:
                        trovato = True
                        break
                if not trovato:
                    response['output'] = 'OK'
                else:
                    response['output'] = 'Esiste già un dispositivo con questo codice'
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('update', 'delete'):
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
    def device_list(role):
        devices = DbManager.select_tb_net_device()
        if role != 'ADMIN':
            for device in devices:
                device['net_usr'] = ''
                device['net_psw'] = ''
        response = {
            'user_role': role,
            'devices': devices,
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_type():
        response = {
            'types': DbManager.select_tb_net_device_type(),
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_command(tipo):
        response = {
            'types': DbManager.select_tb_net_command_from_type(tipo),
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_update(mac, codice, tipo, user, password):
        DbManager.update_tb_net_device(mac, net_code=codice, net_type=tipo, net_user=user, net_psw=password)
        response = {
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_delete(mac):
        DbManager.delete_tb_net_device(mac)
        response = {
            'output': 'OK'
        }
        return response

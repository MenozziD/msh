from controller import BaseHandler
from logging import info, exception
from module import cmd_ping, cmd_wakeonlan, cmd_pcwin_shutdown, cmd_radio, cmd_esp, cmd_netscan, DbManager, set_api_response, validate_format, XmlReader
from netifaces import AF_INET, gateways, ifaddresses


class Net(BaseHandler):

    tipo_operazione = ['scan', 'list', 'type', 'command', 'update', 'delete', 'cmd']
    campi_aggiornabili = ['codice', 'tipo', 'user', 'password']

    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            DbManager()
            response = Net.check(self.session.get('user'), self.session.get('role'), self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                type_op = data['tipo_operazione']
                param = Net.read_param(data)
                funzioni = {
                    'scan': Net.device_scan,
                    'list': Net.device_list,
                    'type': Net.device_type,
                    'command': Net.device_command,
                    'update': Net.device_update,
                    'delete': Net.device_delete,
                    'cmd': Net.device_cmd
                }
                parametri = {
                    'scan': [],
                    'list': [self.session.get('role')],
                    'type': [],
                    'command': [param['tipo']],
                    'update': [param['mac'], param['codice'], param['tipo'], param['user'], param['password']],
                    'delete': [param['mac']],
                    'cmd': [param['dispositivo'], param['comando']]
                }
                response = funzioni[type_op](*parametri[type_op])
            else:
                raise Exception(response['output'])
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            set_api_response(response, self.response)

    @staticmethod
    def read_param(data):
        param = {
            'tipo': None,
            'mac': None,
            'codice': None,
            'user': None,
            'password': None,
            'dispositivo': None,
            'comando': None
        }
        if 'codice' in data:
            param['codice'] = data['codice']
        if 'tipo' in data:
            param['tipo'] = data['tipo']
        if 'mac' in data:
            param['mac'] = data['mac']
        if 'user' in data:
            param['user'] = data['user']
        if 'password' in data:
            param['password'] = data['password']
        if 'dispositivo' in data:
            param['dispositivo'] = data['dispositivo']
        if 'comando' in data:
            param['comando'] = data['comando']
        return param

    @staticmethod
    def check(user, role, request, body):
        response = {}
        if body != "" and validate_format(request):
            data = request.json
            if 'tipo_operazione' in data and data['tipo_operazione'] in ('scan', 'list', 'type', 'command', 'update', 'delete', 'cmd'):
                response = Net.check_user(user, role, data['tipo_operazione'])
                response = Net.check_operation_param(response, data)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 24).replace("%s", "tipo_operazione") + ', '.join(Net.tipo_operazione)
                else:
                    response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 23).replace("%s", "tipo_operazione")
        else:
            if body != "":
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 22)
            else:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 21)
        return response

    @staticmethod
    def check_operation_param(response, data):
        if response['output'] == 'OK':
            if data['tipo_operazione'] == 'command':
                response = Net.check_tipo(data)
            if data['tipo_operazione'] == 'delete':
                response = Net.check_mac(data)
            if data['tipo_operazione'] == 'update':
                response = Net.check_update(data)
            if data['tipo_operazione'] == 'cmd':
                response = Net.check_device(data)
                if response['output'] == 'OK':
                    response = Net.check_command(data)
        return response

    @staticmethod
    def check_update(data):
        response = Net.check_mac(data)
        if response['output'] == 'OK':
            response = Net.check_any_to_update(data)
            if response['output'] == 'OK':
                response = Net.check_tipo(data, required=False)
                if response['output'] == 'OK':
                    response = Net.check_code(data)
        return response

    @staticmethod
    def check_tipo(data, required=True):
        response = {}
        type_list = [d['type_code'] for d in DbManager.select_tb_net_device_type()]
        if 'tipo' in data and data['tipo'] in type_list:
            response['output'] = 'OK'
        else:
            if 'tipo' in data:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 24).replace("%s", "tipo") + ', '.join(type_list)
            else:
                if required:
                    response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 27) + "tipo"
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
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 24).replace("%s", "mac") + ', '.join(mac_list)
            else:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 27) + "mac"
        return response

    @staticmethod
    def check_code(data):
        response = {}
        devices = DbManager.select_tb_net_device()
        to_update = DbManager.select_tb_net_device(data['mac'])[0]
        response['output'] = "OK"
        if 'codice' in data:
            if data['codice'] != "":
                if data['codice'] != to_update['net_code']:
                    response = Net.check_code_exist(data, devices)
            else:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 34)
        return response

    @staticmethod
    def check_code_exist(data, devices):
        trovato = False
        response = {}
        for device in devices:
            if device['net_code'] == data['codice']:
                trovato = True
                break
        if not trovato:
            response['output'] = 'OK'
        else:
            response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 35)
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('update', 'delete'):
                if role != 'ADMIN':
                    response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 26)
                else:
                    response['output'] = 'OK'
            else:
                response['output'] = 'OK'
        else:
            response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 25)
        return response

    @staticmethod
    def check_device(data):
        response = {}
        code_list = [d['net_code'] for d in DbManager.select_tb_net_device()]
        if 'dispositivo' in data and data['dispositivo'] in code_list:
            response['output'] = 'OK'
        else:
            if 'dispositivo' in data:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 24).replace("%s", "dispositivo") + ', '.join(code_list)
            else:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 27) + "dispositivo"
        return response

    @staticmethod
    def check_command(data):
        response = {}
        tipo = DbManager.select_tb_net_device(net_code=data['dispositivo'])[0]
        command_list = [d['cmd_str'] for d in DbManager.select_tb_net_command_from_type(tipo['net_type'])]
        if 'comando' in data and data['comando'] in command_list:
            response['output'] = 'OK'
        else:
            if 'comando' in data:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 24).replace("%s", "comando") + ', '.join(command_list)
            else:
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 27) + "comando"
        return response

    @staticmethod
    def check_any_to_update(data):
        response = {}
        if 'codice' in data or 'tipo' in data or 'user' in data or 'password' in data:
            response['output'] = 'OK'
        else:
            response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 33) + ', '.join(Net.campi_aggiornabili)
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
            'commands': DbManager.select_tb_net_command_from_type(tipo),
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_update(mac, codice=None, tipo=None, user=None, password=None):
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

    @staticmethod
    def device_scan():
        ip = ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['addr'].split('.')
        subnet = ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['netmask'].split('.')
        ip_subnet = Net.calculate_start(ip, subnet)
        response = cmd_netscan(ip_subnet['ip'], ip_subnet['count'])
        if response['output'] == 'OK':
            response = Net.insert_update_device(response)
        return response

    @staticmethod
    def insert_update_device(response):
        inseriti = 0
        aggiornati = 0
        db_devices = DbManager.select_tb_net_device()
        for device in response['devices']:
            trovato = False
            for db_device in db_devices:
                if device['net_mac'] == db_device['net_mac']:
                    DbManager.update_tb_net_device(device['net_mac'], net_ip=device['net_ip'], net_mac_info=device['net_mac_info'])
                    trovato = True
                    aggiornati = aggiornati + 1
                    break
            if not trovato:
                trovato = Net.found_duplicate_code(device)
                if trovato:
                    device['net_code'] = device['net_mac']
                DbManager.insert_tb_net_device(device['net_code'], device['net_ip'], device['net_mac'], device['net_mac_info'])
                inseriti = inseriti + 1
        response['find_device'] = str(len(response['devices']))
        response['new_device'] = str(inseriti)
        response['updated_device'] = str(aggiornati)
        return response

    @staticmethod
    def found_duplicate_code(device):
        trovato = False
        db_devices = DbManager.select_tb_net_device()
        for db_device in db_devices:
            if db_device['net_code'] == device['net_code']:
                trovato = True
                break
        return trovato

    @staticmethod
    def calculate_start(ip, subnet):
        stri = ''
        for s in subnet:
            stri = stri + '{0:08b}'.format(int(s))
        count = stri.count('1')
        if count >= 24:
            ip = ip[0] + '.' + ip[1] + '.' + ip[2] + '.1'
        if 16 <= count < 24:
            ip = ip[0] + '.' + ip[1] + '.0.1'
        if 8 <= count < 16:
            ip = ip[0] + '.0.0.1'
        ip_subnet = {
            'ip': ip,
            'count': str(count)
        }
        return ip_subnet

    @staticmethod
    def device_cmd(dispositivo, comando):
        device_command = DbManager.select_tb_net_device_tb_net_diz_cmd_from_code_and_cmd(dispositivo, comando)
        funzioni = {
            '100': cmd_ping,
            '102': cmd_wakeonlan,
            '130': cmd_esp,
            '201': cmd_pcwin_shutdown,
            '300': cmd_radio,
        }
        parametri = {
            '100': [device_command['net_ip']],
            '102': [device_command['net_mac']],
            '130': [device_command['net_ip'], device_command['cmd_str']],
            '201': [device_command['net_ip'], device_command['net_usr'], device_command['net_psw']],
            '300': [device_command['net_ip'], device_command['cmd_str'].replace("radio_", ""),
                    device_command['net_usr'], device_command['net_psw']]
        }
        return funzioni[device_command['cmd_result']](*parametri[device_command['cmd_result']])

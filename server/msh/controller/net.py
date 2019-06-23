from controller import BaseHandler
from logging import info, exception
from module import cmd_ping, cmd_wakeonlan, cmd_pcwin_shutdown, cmd_radio, cmd_esp, cmd_netscan, XmlReader, DbManager, set_api_response, validate_format
from netifaces import AF_INET, gateways, ifaddresses


class Net(BaseHandler):
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
            DbManager.close_db()
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
                    response['output'] = 'Il campo tipo_operazione deve assumere uno dei seguenti valori: scan, list, type, command, update, delete, cmd'
                else:
                    response['output'] = 'Il campo tipo_operazione è obbligatorio'
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
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
        devices = DbManager.select_tb_net_device()
        to_update = DbManager.select_tb_net_device(data['mac'])[0]
        response['output'] = "OK"
        if 'codice' in data:
            if data['codice'] != "":
                if data['codice'] != to_update['net_code']:
                    response = Net.check_code_exist(data, devices)
            else:
                response['output'] = 'Il campo codice non può essere valorizzato con una stringa vuota'
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
    def check_device(data):
        response = {}
        code_list = [d['net_code'] for d in DbManager.select_tb_net_device()]
        if 'dispositivo' in data and data['dispositivo'] in code_list:
            response['output'] = 'OK'
        else:
            if 'dispositivo' in data:
                response['output'] = "Il campo dispositivo deve assumere uno dei seguenti valori: " + ', '.join(code_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo dispositivo"
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
                response['output'] = "Il campo comando deve assumere uno dei seguenti valori: " + ', '.join(command_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo comando"
        return response

    @staticmethod
    def check_any_to_update(data):
        response = {}
        if 'codice' in data or 'tipo' in data or 'user' in data or 'password' in data:
            response['output'] = 'OK'
        else:
            response['output'] = "Nessun campo da aggiornare, i possibili campi da aggiornare sono codice, tipo, user, password"
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
        response = {}
        inseriti = 0
        aggiornati = 0
        db_devices = DbManager.select_tb_net_device()
        ip_subnet = Net.calculate_start()
        result = cmd_netscan(ip_subnet['ip'], ip_subnet['count'])
        for device in result['devices']:
            trovato = False
            for db_device in db_devices:
                if device['net_mac'] == db_device['net_mac']:
                    DbManager.update_tb_net_device(device['net_mac'], net_status='ON', net_ip=device['net_ip'], net_mac_info=device['net_mac_info'])
                    trovato = True
                    aggiornati = aggiornati + 1
                    break
            if not trovato:
                trovato = Net.found_duplicate_code(device)
                if trovato:
                    device['net_code'] = device['net_mac']
                DbManager.insert_tb_net_device(device['net_code'], device['net_ip'], device['net_mac'], device['net_mac_info'])
                inseriti = inseriti + 1
        Net.update_status_if_not_find(db_devices, result)
        response['output'] = 'OK'
        response['result_command'] = result
        response['find_device'] = str(len(result['devices']))
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
    def calculate_start():
        ip = ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['addr'].split('.')
        subnet = ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['netmask'].split('.')
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
    def update_status_if_not_find(db_devices, result):
        for db_device in db_devices:
            trovato = False
            for device in result['devices']:
                if device['net_mac'] == db_device['net_mac']:
                    trovato = True
                    break
            if not trovato:
                DbManager.update_tb_net_device(db_device['net_mac'], net_status='OFF')

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
        result = funzioni[device_command['cmd_result']](*parametri[device_command['cmd_result']])
        res_decode = DbManager.select_tb_res_decode_from_type_command_lang_value("NET", device_command['cmd_result'], XmlReader.settings['lingua'], result['result'])
        DbManager.update_tb_net_device(device_command['net_mac'], net_status=res_decode['res_state'])
        DbManager.close_db()
        response = result
        response['res_decode'] = res_decode
        return response

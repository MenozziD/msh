from controller import BaseHandler
from logging import info, exception
from module import cmd_ping, cmd_radio, cmd_esp, cmd_netscan, DbManager, set_api_response, validate_format, get_string, get_gateway, cmd_pcwin, cmd_ps4, cmd_pcmac, cmd_reboot
from netifaces import AF_INET, ifaddresses


class Net(BaseHandler):

    tipo_operazione = ['scan', 'list', 'type', 'command', 'update', 'cmd']
    campi_aggiornabili = ['to_delete', 'net_code', 'net_type', 'net_usr', 'net_psw']

    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
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
                    'cmd': Net.device_cmd
                }
                parametri = {
                    'scan': [],
                    'list': [self.session.get('role')],
                    'type': [],
                    'command': [param['net_type']],
                    'update': [param['list_up_device']],
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
            'net_type': None,
            'dispositivo': None,
            'comando': None,
            'list_up_device': None
        }
        if 'net_type' in data:
            param['net_type'] = data['net_type']
        if 'dispositivo' in data:
            param['dispositivo'] = data['dispositivo']
        if 'comando' in data:
            param['comando'] = data['comando']
        if 'list_up_device' in data:
            param['list_up_device'] = data['list_up_device']
        return param

    @staticmethod
    def check(user, role, request, body):
        response = {}
        if body != "" and validate_format(request):
            data = request.json
            if 'tipo_operazione' in data and data['tipo_operazione'] in Net.tipo_operazione:
                response = Net.check_user(user, role, data['tipo_operazione'])
                response = Net.check_operation_param(response, data)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = get_string(24, da_sostiuire="tipo_operazione", da_aggiungere=', '.join(Net.tipo_operazione))
                else:
                    response['output'] = get_string(23, da_sostiuire="tipo_operazione")
        else:
            if body != "":
                response['output'] = get_string(22)
            else:
                response['output'] = get_string(21)
        return response

    @staticmethod
    def check_operation_param(response, data):
        if response['output'] == 'OK':
            if data['tipo_operazione'] == 'command':
                response = Net.check_tipo(data)
            if data['tipo_operazione'] == 'update':
                response = Net.check_update(data)
            if data['tipo_operazione'] == 'cmd':
                response = Net.check_device(data)
                if response['output'] == 'OK':
                    response = Net.check_command(data)
        return response

    @staticmethod
    def check_update(data):
        response = {}
        error = False
        if 'list_up_device' in data and data['list_up_device'] != []:
            for device in data['list_up_device']:
                if error is False:
                    response = Net.check_mac(device)
                    if response['output'] == 'OK':
                        response = Net.check_any_to_update(device)
                        if response['output'] == 'OK':
                            response = Net.check_to_delete(device)
                            if response['output'] == 'NO':
                                response = Net.check_tipo(device, required=False)
                                if response['output'] == 'OK':
                                    response = Net.check_code(device)
                                    if response['output'] != 'OK':
                                        error = True
                                else:
                                    error = True
                            else:
                                if response['output'] != 'OK':
                                    error = True
                        else:
                            error = True
                    else:
                        error = True
                else:
                    break
        else:
            if 'list_up_device' in data:
                response['output'] = get_string(24, da_sostiuire="list_up_device", da_aggiungere='non lista vuota')
            else:
                response['output'] = get_string(27, da_aggiungere="list_up_device")
        return response

    @staticmethod
    def check_to_delete(data):
        response = {
            'output': "NO"
        }
        if 'to_delete' in data and data['to_delete'] in (True, False):
            response['output'] = 'OK'
        else:
            if 'to_delete' in data:
                response['output'] = get_string(24, da_sostiuire="to_delete", da_aggiungere='true, false')
        return response

    @staticmethod
    def check_tipo(data, required=True):
        response = {}
        type_list = [d['type_code'] for d in DbManager.select_tb_net_device_type()]
        if 'net_type' in data and data['net_type'] in type_list:
            response['output'] = 'OK'
        else:
            if 'net_type' in data:
                response['output'] = get_string(24, da_sostiuire="net_type", da_aggiungere=', '.join(type_list))
            else:
                if required:
                    response['output'] = get_string(27, da_aggiungere="net_type")
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def check_mac(data):
        response = {}
        mac_list = [d['net_mac'] for d in DbManager.select_tb_net_device()]
        if 'net_mac' in data and data['net_mac'] in mac_list:
            response['output'] = 'OK'
        else:
            if 'net_mac' in data:
                response['output'] = get_string(24, da_sostiuire="net_mac", da_aggiungere=', '.join(mac_list))
            else:
                response['output'] = get_string(27, da_aggiungere="net_mac")
        return response

    @staticmethod
    def check_code(data):
        response = {}
        devices = DbManager.select_tb_net_device()
        to_update = DbManager.select_tb_net_device(data['net_mac'])[0]
        response['output'] = "OK"
        if 'net_code' in data:
            if data['net_code'] != "":
                if data['net_code'] != to_update['net_code']:
                    response = Net.check_code_exist(data, devices)
            else:
                response['output'] = get_string(34, da_sostiuire="net_code")
        return response

    @staticmethod
    def check_code_exist(data, devices):
        trovato = False
        response = {}
        for device in devices:
            if device['net_code'] == data['net_code']:
                trovato = True
                break
        if not trovato:
            response['output'] = 'OK'
        else:
            response['output'] = get_string(35)
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('update', 'delete'):
                if role != 'ADMIN':
                    response['output'] = get_string(26)
                else:
                    response['output'] = 'OK'
            else:
                response['output'] = 'OK'
        else:
            response['output'] = get_string(25)
        return response

    @staticmethod
    def check_device(data):
        response = {}
        code_list = [d['net_code'] for d in DbManager.select_tb_net_device()]
        if 'dispositivo' in data and data['dispositivo'] in code_list:
            response['output'] = 'OK'
        else:
            if 'dispositivo' in data:
                response['output'] = get_string(24, da_sostiuire="dispositivo", da_aggiungere=', '.join(code_list))
            else:
                response['output'] = get_string(27, da_aggiungere="dispositivo")
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
                response['output'] = get_string(24, da_sostiuire="comando", da_aggiungere=', '.join(command_list))
            else:
                response['output'] = get_string(27, da_aggiungere="comando")
        return response

    @staticmethod
    def check_any_to_update(data):
        response = {}
        if 'net_code' in data or 'net_type' in data or 'net_usr' in data or 'net_psw' in data or 'to_delete' in data:
            response['output'] = 'OK'
        else:
            response['output'] = get_string(33, da_aggiungere=', '.join(Net.campi_aggiornabili))
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
    def device_update(list_device):
        for device in list_device:
            if Net.check_to_delete(device)['output'] == 'OK':
                DbManager.delete_tb_net_device(device['net_mac'])
            else:
                codice = None
                tipo = None
                user = None
                password = None
                if 'net_code' in device:
                    codice = device['net_code']
                if 'net_type' in device:
                    tipo = device['net_type']
                if 'net_usr' in device:
                    user = device['net_usr']
                if 'net_psw' in device:
                    password = device['net_psw']
                DbManager.update_tb_net_device(device['net_mac'], net_code=codice, net_type=tipo, net_user=user, net_psw=password)
        response = {
            'output': 'OK'
        }
        return response

    @staticmethod
    def device_scan():
        gateway = get_gateway()
        ip = ifaddresses(gateway)[AF_INET][0]['addr'].split('.')
        subnet = ifaddresses(gateway)[AF_INET][0]['netmask'].split('.')
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
        device_command = DbManager.select_device_and_function_code_from_code_and_cmd(dispositivo, comando)
        funzioni = {
            '1': cmd_ping,
            '2': cmd_pcwin,
            '3': cmd_radio,
            '4': cmd_esp,
            '5': cmd_ps4,
            '6': cmd_pcmac,
            '7': cmd_reboot
        }
        parametri = {
            '1': [device_command['net_ip']],
            '2': [comando, device_command['net_mac'], device_command['net_ip'], device_command['net_usr'], device_command['net_psw']],
            '3': [device_command['net_ip'], comando, device_command['net_usr'], device_command['net_psw']],
            '4': [device_command['net_ip'], comando],
            '5': [comando],
            '6': [comando, device_command['net_mac'], device_command['net_ip'], device_command['net_usr'],
                  device_command['net_psw']],
            '7': [device_command['net_ip'], device_command['net_usr'], device_command['net_psw']]
        }
        return funzioni[device_command['function_code']](*parametri[device_command['function_code']])

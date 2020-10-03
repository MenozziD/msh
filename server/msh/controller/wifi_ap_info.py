from json import loads
from controller import BaseHandler
from logging import info, exception
from controller import Net
from module import DbManager, add_user, delete_user, update_user, set_api_response, validate_format, get_string, wifi_ap_info


class WiFiInfo(BaseHandler):

    tipo_operazione = ['list', 'update']

    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            response = WiFiInfo.check(self.session.get('user'), self.session.get('role'), self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                tipo_operazione = data['tipo_operazione']
                wifi = None
                if 'wifi' in data:
                    wifi = data['wifi']
                funzioni = {
                    'list': WiFiInfo.wifi_list,
                    'update': WiFiInfo.wifi_update,
                }
                parametri = {
                    'list': [],
                    'update': [wifi],
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
            if 'tipo_operazione' in data and data['tipo_operazione'] in WiFiInfo.tipo_operazione:
                response = WiFiInfo.check_user(user, role)
                response = WiFiInfo.check_operation_param(response, data)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = get_string(24, da_sostiuire="tipo_operazione", da_aggiungere=', '.join(WiFiInfo.tipo_operazione))
                else:
                    response['output'] = get_string(23, da_sostiuire="tipo_operazione")
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
                response = WiFiInfo.check_update(data)
        return response

    @staticmethod
    def check_update(data):
        response = {}
        if 'wifi' in data and 'ssid' in data['wifi'] and 'psw' in data['wifi'] and data['wifi']['ssid'] != '' and data['wifi']['psw'] != '':
            response['output'] = 'OK'
        else:
            if 'wifi' in data:
                if 'ssid' in data['wifi']:
                    response['output'] = get_string(27, da_aggiungere="wifi.ssid")
                else:
                    response['output'] = get_string(34, da_sostituire="wifi.ssid")
                if 'psw' in data['wifi']:
                    response['output'] = get_string(27, da_aggiungere="wifi.psw")
                else:
                    response['output'] = get_string(34, da_sostituire="wifi.psw")
            else:
                response['output'] = get_string(27, da_aggiungere="wifi")
        return response

    @staticmethod
    def wifi_list():
        response = {}
        ap_list = DbManager.select_tb_net_device_and_msh_info(net_type='AP')
        db_devices = DbManager.select_tb_net_device_and_msh_info()
        wifi_ap_all_list = []
        for ap in ap_list:
            wifi_info = wifi_ap_info(ap['net_ip'], ap['net_usr'], ap['net_psw'], ap['net_code'])
            if wifi_info['output'] == 'OK':
                for wifi in wifi_info['result']:
                    trovato = False
                    for db_device in db_devices:
                        if wifi['ssid'] == db_device['net_mac']:
                            DbManager.update_tb_net_device(wifi['ssid'], net_ip=ap['net_ip'], net_user=ap['net_usr'], net_psw=ap['net_psw'])
                            trovato = True
                            break
                    if not trovato:
                        wifi['net_code'] = wifi['ssid']
                        wifi['net_mac_info'] = ap['net_mac']
                        trovato = Net.found_duplicate_code(wifi)
                        if trovato:
                            wifi['net_code'] = "SSID duplicato"
                        DbManager.insert_tb_net_device(wifi['ssid'], ap['net_ip'], wifi['ssid'],
                                                       wifi['net_mac_info'], net_usr=ap['net_usr'], net_psw=ap['net_psw'])
                wifi_ap_all_list = wifi_ap_all_list + wifi_info['result']
        response['wifi_ap'] = wifi_ap_all_list
        wifi = DbManager.select_tb_wifi()
        if not wifi:
            response['default_ap'] = ""
        else:
            response['default_ap'] = wifi[0]
        response['output'] = 'OK'
        return response

    @staticmethod
    def wifi_update(wifi):
        response = {}
        if DbManager.select_tb_wifi():
            DbManager.delete_tb_wifi()
        DbManager.insert_tb_wifi(wifi['ssid'], wifi['psw'])
        response['output'] = 'OK'
        return response

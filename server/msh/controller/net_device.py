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
            if self.session.get('user') is not None:
                data = loads(body)
                type_op = data['tipo_operazione']
                codice = data['codice']
                tipo = data['tipo']
                mac = data['mac']
                user = data['user']
                password = data['password']
                DbManager()
                if type_op == 'list':
                    devices = DbManager.select_tb_net_device()
                    if self.session.get('role') != 'ADMIN':
                        for device in devices:
                            device['net_usr'] = ''
                            device['net_psw'] = ''
                    response['user_role'] = self.session.get('role')
                    response['devices'] = devices
                    response['output'] = 'OK'
                if type_op == 'type':
                    response['types'] = DbManager.select_tb_net_device_type()
                    response['output'] = 'OK'
                if type_op == 'command':
                    response['commands'] = DbManager.select_tb_net_command_from_type(tipo)
                    response['output'] = 'OK'
                if type_op == 'update':
                    if self.session.get('role') == 'ADMIN':
                        devices = DbManager.select_tb_net_device()
                        to_update = DbManager.select_tb_net_device(mac)
                        if len(to_update) == 1:
                            to_update = to_update[0]
                            if codice != to_update['net_code']:
                                trovato = False
                                for device in devices:
                                    if device['net_code'] == codice:
                                        trovato = True
                                        break
                                if not trovato:
                                    DbManager.update_tb_net_device(mac, net_code=codice, net_type=tipo, net_user=user, net_psw=password)
                                    response['output'] = 'OK'
                                else:
                                    response['output'] = 'Esiste già un dispositivo con questo codice'
                            else:
                                DbManager.update_tb_net_device(mac, net_code=codice, net_type=tipo, net_user=user, net_psw=password)
                                response['output'] = 'OK'
                        else:
                            response['output'] = 'Non esiste nessun device con questo mac address'
                    else:
                        response['output'] = 'Solo gli ADMIN possono aggiornare i dispositivi'
                if type_op == 'delete':
                    if self.session.get('role') == 'ADMIN':
                        DbManager.delete_tb_net_device(mac)
                        response['output'] = 'OK'
                    else:
                        response['output'] = 'Solo gli ADMIN possono rimuovere i dispositivi'
                DbManager.close_db()
            else:
                response['output'] = 'Devi effettuare la login per utilizzare questa API'
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

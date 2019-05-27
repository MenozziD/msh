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
        if self.session.get('user') is not None:
            response = {}
            try:
                data = loads(body)
                type_op = data['tipo_operazione']
                codice = data['codice']
                tipo = data['tipo']
                mac = data['mac']
                user = data['user']
                password = data['password']
                DbManager()
                if type_op == 'list':
                    response['devices'] = DbManager.select_tb_net_device()
                if type_op == 'type':
                    response['types'] = DbManager.select_tb_net_device_type()
                if type_op == 'command':
                    response['commands'] = DbManager.select_tb_net_command_from_type(tipo)
                if type_op == 'update':
                    DbManager.update_tb_net_device(mac, net_code=codice, net_type=tipo, net_user=user, net_psw=password)
                DbManager.close_db()
                response['output'] = 'OK'
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
        else:
            self.redirect('/static/page/login.html')
            info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])

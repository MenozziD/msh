from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.xml_reader import XmlReader
from json import dumps, loads
from datetime import datetime


class NetDevice(RequestHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            data = loads(body)
            type_op = data['tipo_operazione']
            codice = data['codice']
            tipo = data['tipo']
            mac = data['mac']
            DbManager(XmlReader.settings['path']['db'])
            if type_op == 'list':
                rows = DbManager.select(XmlReader.settings['query']['select_tb_net_device'])
                response['devices'] = DbManager.tb_net_device(rows)
            if type_op == 'type':
                rows = DbManager.select(XmlReader.settings['query']['select_tb_net_device_type'])
                response['types'] = DbManager.tb_net_device_type(rows)
            if type_op == 'command':
                rows = DbManager.select(XmlReader.settings['query']['select_net_command_for_type'] % tipo)
                response['commands'] = DbManager.tb_net_diz_cmd(rows)
            if type_op == 'update':
                rows = DbManager.select(XmlReader.settings['query']['select_tb_net_device_from_mac'] % mac)
                device = DbManager.tb_net_device(rows)[0]
                DbManager.insert_or_update(XmlReader.settings['query']['update_tb_net_device'] % (codice, tipo, device['net_status'], device['net_ip'], device['net_mac_info'], device['net_mac']))
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

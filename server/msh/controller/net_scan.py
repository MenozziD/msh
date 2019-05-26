from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.xml_reader import XmlReader
from module.net import cmd_netscan, get_ip_and_subnet
from json import dumps
from datetime import datetime


class NetScan(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        inseriti = 0
        aggiornati = 0
        response = {
            'output': '',
            'result_command': '',
            'find_device': '',
            'new_device': '',
            'updated_device': '',
            'timestamp': ''
        }
        try:
            DbManager()
            db_devices = DbManager.select_tb_net_device()
            ip_subnet = get_ip_and_subnet()
            ip = ip_subnet['ip'].split('.')
            subnet = ip_subnet['subnet'].split('.')
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
            info("PARTO DA %s/%s", ip, str(count))
            result = cmd_netscan(ip, str(count))
            for device in result['devices']:
                trovato = False
                for db_device in db_devices:
                    if device['net_mac'] == db_device['net_mac']:
                        DbManager.update_tb_net_device(device['net_mac'], net_status='ON', net_ip=device['net_ip'], net_mac_info=device['net_mac_info'])
                        trovato = True
                        aggiornati = aggiornati + 1
                        break
                if not trovato:
                    DbManager.insert_tb_net_device(device['net_code'], 'NET', 'ON', device['net_ip'], '', '', device['net_mac'], device['net_mac_info'])
                    inseriti = inseriti + 1
            for db_device in db_devices:
                trovato = False
                for device in result['devices']:
                    if device['net_mac'] == db_device['net_mac']:
                        trovato = True
                        break
                if not trovato:
                    DbManager.update_tb_net_device(db_device['net_mac'], net_status='OFF')
            DbManager.close_db()
            response['output'] = 'OK'
            response['result_command'] = result
            response['find_device'] = str(len(result['devices']))
            response['new_device'] = str(inseriti)
            response['updated_device'] = str(aggiornati)
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

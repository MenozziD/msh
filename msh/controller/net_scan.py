from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.utility import XmlReader
from module.net import cmd_netscan, get_ip_and_subnet
from json import dumps
from datetime import datetime
from socket import gethostbyname, gethostname


class NetScan(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        db_devices = []
        inseriti = 0
        aggiornati = 0
        response = {
            'output': '',
            'find_device': '',
            'new_device': '',
            'updated_device': '',
            'timestamp': ''
        }
        try:
            DbManager(XmlReader.settings['path']['db'])
            rows = DbManager.select(DbManager.select(XmlReader.settings['query']['select_tb_net_device']))
            for r in rows:
                device = {'net_code': str(r[0]),
                          'net_type': str(r[1]),
                          'net_status': str(r[2]),
                          'net_ip': str(r[4]),
                          'net_mac': str(r[5]),
                          'net_mac_info': str(r[6])
                          }
                db_devices.append(device)
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
            if len(result['devices'] > 0):
                for device in result['devices']:
                    trovato = False
                    if len(db_devices) > 0:
                        for db_device in db_devices:
                            if device['net_mac'] == db_device['net_mac']:
                                DbManager.insert_or_update(XmlReader.settings['query']['update_tb_net_device'] % (db_device['net_code'], db_device['net_type'], db_device['net_status'], device['net_ip'], device['net_mac'], device['net_mac_info']))
                                trovato = True
                                aggiornati = aggiornati + 1
                    if not trovato:
                        DbManager.insert_or_update(XmlReader.settings['query']['insert_tb_net_device'] % (device['net_code'], 'NET', 'ON', device['net_ip'], device['net_mac'], device['net_mac_info']))
                        inseriti = inseriti + 1
            DbManager.close_db()
            response['output'] = 'OK'
            response['find_device'] = str(len(result['device']))
            response['new_device'] = str(inseriti)
            response['updated_device'] = str(aggiornati)
            info("INSERITI: %s AGGIORNATI: %s", str(inseriti), str(aggiornati))
        except Exception as e:
            exception("Exception")
            response['output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['net'], e)
        finally:
            response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            info("RESPONSE CODE: %s", self.response.status)
            info("RESPONSE PAYLOAD: %s", response)

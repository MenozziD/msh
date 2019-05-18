from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.xml_reader import XmlReader
from json import dumps
from datetime import datetime


class DeviceList(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        response = {}
        try:
            DbManager(XmlReader.settings['path']['db'])
            rows = DbManager.select(XmlReader.settings['query']['select_tb_net_device'])
            devices = []
            for r in rows:
                device = {'device_code': str(r[0]),
                          'device_type': str(r[1]),
                          'device_status': str(r[2]),
                          'device_ip': str(r[4]),
                          'device_mac': str(r[5]),
                          'device_mac_info': str(r[6])
                          }
                devices.append(device)
            DbManager.close_db()
            response['output'] = 'OK'
            response['devices'] = devices
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

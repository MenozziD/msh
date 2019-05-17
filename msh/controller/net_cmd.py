from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.utility import XmlReader
from module.net import cmd_ping, cmd_wakeonlan, cmd_pcwin_shutdown, cmd_radiostatus, cmd_radioctrl
from json import dumps
from datetime import datetime


class NetCmd(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        response = {}
        try:
            dispositivo = self.request.get('d')
            comando = self.request.get('c')
            DbManager(XmlReader.settings['path']['db'])
            r = DbManager.select(DbManager.select(XmlReader.settings['query']['select_tb_net_diz_cmd'] % (dispositivo, comando)))
            response = {'device_code': str(r[0]),
                        'device_type': str(r[1]),
                        'device_ip': str(r[2]),
                        'device_mac': str(r[3]),
                        'device_user': str(r[6]),
                        'device_psw': str(r[7]),
                        'device_strcmd': str(r[4]),
                        'device_rescmd': str(r[5]),
                        'output_command': '',
                        'output': '',
                        'req_response': '',
                        'device_status': '',
                        'timestamp': '',
                        }
            funzioni = {
                '100': cmd_ping,
                '102': cmd_wakeonlan,
                '201': cmd_pcwin_shutdown,
                '300': cmd_radiostatus,
                '301': cmd_radioctrl,
                '302': cmd_radioctrl
            }
            parametri = {
                '100': [response['device_ip']],
                '102': [response['device_mac']],
                '201': [response['device_ip'], response['device_user'], response['device_psw']],
                '300': [response['device_ip'], response['device_user'], response['device_psw']],
                '301': [response['device_ip'], response['device_strcmd'].replace("radio_", ""), response['device_user'], response['device_psw']],
                '302': [response['device_ip'], response['device_strcmd'].replace("radio_", ""), response['device_user'], response['device_psw']]
            }
            result = funzioni[response['device_rescmd']](*parametri[response['device_rescmd']])
            row = DbManager.select(XmlReader.settings['query']['select_one_tb_res_decode'] % ("NET", response['device_type'], response['device_rescmd'], XmlReader.settings['lingua'], result['result']))
            if row != "":
                response['req_response'] = str(row[0])
                response['device_status'] = str(row[1])
            else:
                response['req_response'] = "-"
                response['device_status'] = "-"
            response['output_command'] = result
            response['output'] = 'OK'
            DbManager.close_db()
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

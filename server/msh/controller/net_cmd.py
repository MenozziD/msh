from controller import BaseHandler
from logging import info, exception
from module import DbManager
from module import XmlReader
from module import cmd_ping, cmd_wakeonlan, cmd_pcwin_shutdown, cmd_radio, cmd_esp
from json import dumps, loads
from datetime import datetime


class NetCmd(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        if self.session.get('user') is not None:
            response = {}
            try:
                data = loads(body)
                dispositivo = data['dispositivo']
                comando = data['comando']
                DbManager()
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
                    '300': [device_command['net_ip'], device_command['cmd_str'].replace("radio_", ""), device_command['net_usr'], device_command['net_psw']]
                }
                result = funzioni[device_command['cmd_result']](*parametri[device_command['cmd_result']])
                res_decode = DbManager.select_tb_res_decode_from_type_command_lang_value("NET", device_command['cmd_result'], XmlReader.settings['lingua'], result['result'])
                DbManager.update_tb_net_device(device_command['net_mac'], net_status=res_decode['res_state'])
                DbManager.close_db()
                response['output'] = 'OK'
                response['result_command'] = result
                response['res_decode'] = res_decode
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

import webapp3
import logging
import socket
from paste import httpserver
from datetime import datetime
from json import dumps, loads
from module.dbmanager import DbManager
from module.utility import XmlReader
from module import net


class NetScan(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        device = {'net_code': '',
                  'net_type': '',
                  'net_status': '',
                  'net_ip': '',
                  'net_mac': '',
                  'net_mac_info': ''
                  }
        db_devices = []
        response = {}
        try:

            DbManager(XmlReader.settings['path']['db'])
            rows = DbManager.select_tb_net_device()
            for r in rows:
                device = {'net_code': str(r[0]),
                          'net_type': str(r[1]),
                          'net_status': '',
                          'net_ip': str(r[2]),
                          'net_mac': str(r[3]),
                          'net_mac_info': ''
                          }
                db_devices.append(device)

            result = net.cmd_netscan()
            '''
            for device in result['devices']:
                for db_device in db_devices:
                    if device['net_mac'] == db_device['net_mac']:
                        logging.info("UPDATE")
                        DbManager.update_tb_net_device(device['net_code'], '', 'ON', device['net_ip'],
                                                       device['net_mac'], device['net_mac_info'])
                    else:
                        logging.info("INSERT")
                        DbManager.insert_tb_net_device(device['net_code'], '', 'ON', device['net_ip'], device['net_mac'],
                                                       device['net_mac_info'])
            '''

            response = result['devices']

            DbManager.close_db()
        except Exception as e:
            response['output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['net'], e)
        finally:
            #response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            logging.info("RESPONSE CODE: %s", self.response.status)
            logging.info("RESPONSE PAYLOAD: %s", response)

            
class NetCmd(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        response = {}
        try:
            dispositivo = self.request.get('d')
            comando = self.request.get('c')
            DbManager(XmlReader.settings['path']['db'])
            result = {}
            r = DbManager.select_tb_net_diz_cmd(dispositivo, comando)
            response = {'device_code': str(r[0]),
                        'device_type': str(r[1]),
                        'device_ip': str(r[2]),
                        'device_mac': str(r[3]),
                        'device_user': str(r[6]),
                        'device_psw': str(r[7]),
                        'device_strcmd': str(r[4]),
                        'device_rescmd': str(r[5]),
                        'output': '',
                        'req_response': '',
                        'device_status': '',
                        'timestamp': '',
                        }
            if response['device_rescmd'] == "100":
                result = net.cmd_ping(response['device_ip'])
            if response['device_rescmd'] == "102":
                result = net.cmd_wakeonlan(response['device_mac'])
            if response['device_rescmd'] == "201":
                result = net.cmd_pcwin_shutdown(response['device_ip'], response['device_user'], response['device_psw'])
            if response['device_rescmd'] == "300":
                result = net.cmd_radiostatus(response['device_ip'], response['device_user'], response['device_psw'])
            if response['device_rescmd'] in ("301", "302"):
                result = net.cmd_radioctrl(response['device_ip'], response['device_strcmd'].replace("radio_", ""), response['device_user'], response['device_psw'])
            row = DbManager.select_one_tb_res_decode("NET", response['device_type'], response['device_rescmd'], XmlReader.settings['lingua'], result['result'])
            if row != "":
                response['req_response'] = str(row[0])
                response['device_status'] = str(row[1])
            else:
                response['req_response'] = "-"
                response['device_status'] = "-"
            response['output'] = result
            DbManager.close_db()
        except Exception as e:
            response['output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['net'], e)
        finally:
            response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            logging.info("RESPONSE CODE: %s", self.response.status)
            logging.info("RESPONSE PAYLOAD: %s", response)


class Index(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        self.redirect(XmlReader.settings['path']['index'])
        logging.info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])


class Static(webapp3.RequestHandler):
    def get(self, filename):
        path_ui = XmlReader.settings['path']['ui']
        logging.info("%s %s", self.request.method, self.request.url)
        f = open(path_ui + filename, 'r')
        self.response.write(f.read())
        f.close()
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: %s%s", path_ui, filename)


class Diff(webapp3.RequestHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        logging.info("%s %s", self.request.method, self.request.url)
        logging.info("BODY %s", body)
        data = loads(body)
        res = int(data['primo']) - int(data['secondo'])
        self.response.write(res)
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: %s", res)


def handle_error(request, response, exception):
    path_error = XmlReader.settings['path']['error']
    error_code = '500'
    for code, value in XmlReader.settings['class_error'].items():
        if str(value) == str(type(exception)):
            error_code = code
    if error_code != '500':
        logging.info("%s %s", request.method, request.url)
    logging.exception(exception)
    f = open(path_error + error_code + '.html', 'r')
    response.write(f.read())
    response.set_status(int(error_code))
    f.close()
    logging.info("RESPONSE CODE: %s", response.status)
    logging.info("RESPONSE PAYLOAD: %s%s.html", path_error, error_code)


app = webapp3.WSGIApplication([
    ('/api/netcmd', NetCmd),
    ('/api/netscan', NetScan),
    ('/api/diff', Diff),
    ('/', Index),
    (r'/static/(\D+)', Static),
], debug=True)
app.error_handlers[404] = handle_error
app.error_handlers[405] = handle_error
app.error_handlers[500] = handle_error


def main():
    XmlReader()
    logging.basicConfig(
        filename=XmlReader.settings['log']['filename'],
        format=XmlReader.settings['log']['format'],
        level=XmlReader.settings['log']['level'])
    #ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = '192.168.1.111'
    logging.info("Your Computer IP Address is %s", ip_address)
    port = XmlReader.settings['porta']
    logging.info("Server in ascolto su http://%s:%s", ip_address, port)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

import webapp3
import logging
from paste import httpserver
from datetime import datetime
from json import dumps, loads
from module import net, dbmanager
import socket


class NetCmd(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        response = {}
        try:
            dispositivo = self.request.get('d')
            comando = self.request.get('c')
            db = dbmanager.open_db("db/system.db")
            result = {}

            r = dbmanager.select_tb_net_diz_cmd(db, dispositivo, comando)
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
                result = net.cmd_radioctrl(response['device_ip'], response['device_strcmd'].replace("radio_", ""),
                                           response['device_user'], response['device_psw'])

            # Calcolo Stringa Response e Stringa Stato Dispositivo e aggiorno struttura
            row = dbmanager.select_one_tb_res_decode(db, "NET", response['device_type'], response['device_rescmd'],
                                                     "IT", result['result'])

            if row != "":
                response['req_response'] = str(row[0])
                response['device_status'] = str(row[1])
            else:
                response['req_response'] = "-"
                response['device_status'] = "-"

            response['output'] = result
            dbmanager.close_db(db)

        except Exception as e:
            response['output'] = "Error-%s:%s " % ("net_cmd", e)
        finally:
            response['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            logging.info("RESPONSE CODE: %s", self.response.status)
            logging.info("RESPONSE PAYLOAD: %s", response)


class Index(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        self.redirect('/static/page/index.html')
        logging.info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])


class Static(webapp3.RequestHandler):
    def get(self, filename):
        logging.info("%s %s", self.request.method, self.request.url)
        f = open('webui/' + filename, 'r')
        self.response.write(f.read())
        f.close()
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: webui/%s", filename)


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


path_error = 'webui/page/error/'


def handle_404(request, response, exception):
    error_code = '404'
    logging.info("%s %s", request.method, request.url)
    logging.exception(exception)
    f = open(path_error + error_code + '.html', 'r')
    response.write(f.read())
    response.set_status(int(error_code))
    f.close()
    logging.info("RESPONSE CODE: %s", response.status)
    logging.info("RESPONSE PAYLOAD: %s%s.html", path_error, error_code)


def handle_405(request, response, exception):
    error_code = '405'
    logging.info("%s %s", request.method, request.url)
    logging.exception(exception)
    f = open(path_error + error_code + '.html', 'r')
    response.write(f.read())
    response.set_status(int(error_code))
    f.close()
    logging.info("RESPONSE CODE: %s", response.status)
    logging.info("RESPONSE PAYLOAD: %s%s.html", path_error, error_code)


def handle_500(request, response, exception):
    error_code = '500'
    logging.exception(exception)
    f = open(path_error + error_code + '.html', 'r')
    response.write(f.read())
    response.set_status(int(error_code))
    f.close()
    logging.info("RESPONSE CODE: %s", response.status)
    logging.info("RESPONSE PAYLOAD: %s%s.html", path_error, error_code)


app = webapp3.WSGIApplication([
    ('/api/netcmd', NetCmd),
    ('/', Index),
    (r'/static/(\D+)', Static),
    (r'/api/diff', Diff),
], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405
app.error_handlers[500] = handle_500


def main():
    logging.basicConfig(
        # filename='msh.log',
        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
        level=logging.INFO)
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    logging.info("Your Computer Name is: %s", hostname)
    logging.info("Your Computer IP Address is %s", IPAddr)
    port = '65177'
    logging.info("Server in ascolto su http://%s:%s", IPAddr, port)
    httpserver.serve(app, host=IPAddr, port=port)


if __name__ == '__main__':
    main()

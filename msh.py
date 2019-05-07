import webapp3
from paste import httpserver
from datetime import datetime
from json import dumps
from module import net, dbmanager


class NetCmd(webapp3.RequestHandler):
    def get(self):
        response = {}
        try:
            dispositivo = self.request.GET['d']
            comando = self.request.GET['c']
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


class Index(webapp3.RequestHandler):
    def get(self):
        print("ACCESSO ALLA HOME")
        f = open('webui/index.html', 'r')
        self.response.write(f.read())
        f.close()


class Static(webapp3.RequestHandler):
    def get(self, filename):
        print("REQUEST FILE:", filename)
        f = open('webui/' + filename, 'r')
        self.response.write(f.read())
        f.close()


app = webapp3.WSGIApplication([
    ('/api/netcmd', NetCmd),
    ('/', Index),
    (r'/static/(\D+)', Static),
], debug=True)


def main():
    httpserver.serve(app, host='192.168.1.111', port='65177')


if __name__ == '__main__':
    main()

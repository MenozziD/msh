from webapp3 import RequestHandler, WSGIApplication
from paste import httpserver
from socket import gethostname, gethostbyname
from json import dumps
from logging import INFO, basicConfig, info


class ReleStato(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": ""
        }
        f = open("rele.txt", "r")
        data["stato"] = f.read()
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", data)


class ReleOn(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": "ON"
        }
        f = open("rele.txt", "w")
        f.write("ON")
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", data)


class ReleOff(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": "OFF"
        }
        f = open("rele.txt", "w")
        f.write("OFF")
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", data)


app = WSGIApplication([
    ('/rele_stato', ReleStato),
    ('/rele_on', ReleOn),
    ('/rele_off', ReleOff),
], debug=True)


def main():
    f = open("rele.txt", "w")
    f.write("OFF")
    f.close()
    basicConfig(
        filename="esp_rele.log",
        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
        level=INFO)
    ip_address = gethostbyname(gethostname())
    info("Your Computer IP Address is %s", ip_address)
    port = "8080"
    info("Server in ascolto su http://%s:%s", ip_address, port)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

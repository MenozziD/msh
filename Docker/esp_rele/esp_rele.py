import webapp3
from paste import httpserver
import socket
from json import dumps
import logging


class ReleStato(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": ""
        }
        f = open("rele.txt", "r")
        data["stato"] = f.read()
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: %s", data)


class ReleOn(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": "ON"
        }
        f = open("rele.txt", "w")
        f.write("ON")
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: %s", data)


class ReleOff(webapp3.RequestHandler):
    def get(self):
        logging.info("%s %s", self.request.method, self.request.url)
        data = {
            "stato": "OFF"
        }
        f = open("rele.txt", "w")
        f.write("OFF")
        f.close()
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(data, indent=4, sort_keys=True))
        logging.info("RESPONSE CODE: %s", self.response.status)
        logging.info("RESPONSE PAYLOAD: %s", data)


app = webapp3.WSGIApplication([
    ('/rele_stato', ReleStato),
    ('/rele_on', ReleOn),
    ('/rele_off', ReleOff),
], debug=True)


def main():
    f = open("rele.txt", "w")
    f.write("OFF")
    f.close()
    logging.basicConfig(
        filename="esp_rele.log",
        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
        level=logging.INFO)
    ip_address = socket.gethostbyname(socket.gethostname())
    logging.info("Your Computer IP Address is %s", ip_address)
    port = "8080"
    logging.info("Server in ascolto su http://%s:%s", ip_address, port)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

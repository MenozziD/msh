from controller import BaseHandler
from os import system
from json import dumps
from logging import info
from datetime import datetime
from module import XmlReader


class UpdateLastVersion(BaseHandler):
    def get(self):
        response = {}
        info("%s %s", self.request.method, self.request.url)
        if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
            system("sudo python3 deploy.py 1>/dev/null 2>/dev/null &")
            response['output'] = 'OK'
        else:
            response['output'] = 'Devi effettuare la login per utilizzare questa API'
            if self.session.get('role') == 'USER':
                response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
        response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(response, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", response)

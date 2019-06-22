from controller import BaseHandler
from json import dumps
from logging import info
from datetime import datetime
from module import XmlReader
from module import execute_os_cmd


class UpdateLastVersion(BaseHandler):
    def get(self):
        response = {}
        info("%s %s", self.request.method, self.request.url)
        if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
            response['output'] = 'OK'
            cmd = "cd .. && sudo ./deploy.sh &"
            execute_os_cmd(cmd)
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

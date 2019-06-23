from controller import BaseHandler
from logging import info
from module import execute_os_cmd, set_api_response


class UpdateLastVersion(BaseHandler):
    def get(self):
        response = {}
        info("%s %s", self.request.method, self.request.url)
        if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
            response['output'] = 'OK'
            cmd = "cd .. && sudo ./deploy.sh &"
            execute_os_cmd(cmd, sys=True)
        else:
            response['output'] = 'Devi effettuare la login per utilizzare questa API'
            if self.session.get('role') == 'USER':
                response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
        set_api_response(response, self.response)

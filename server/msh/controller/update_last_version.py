from controller import BaseHandler
from logging import info
from module import execute_os_cmd, set_api_response, get_string, DbManager


class UpdateLastVersion(BaseHandler):
    def get(self):
        response = {}
        info("%s %s", self.request.method, self.request.url)
        if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
            response['output'] = 'OK'
            ret = execute_os_cmd("cd .. && sudo ./deploy.sh &")
            if ret['cmd_err'] != "":
                response['output'] = 'KO'
        else:
            response['output'] = get_string(25)
            if self.session.get('role') == 'USER':
                response['output'] = get_string(26)
        set_api_response(response, self.response)

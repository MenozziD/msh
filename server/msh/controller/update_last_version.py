from controller import BaseHandler
from logging import info
from module import execute_os_cmd, set_api_response, XmlReader, DbManager


class UpdateLastVersion(BaseHandler):
    def get(self):
        response = {}
        info("%s %s", self.request.method, self.request.url)
        DbManager()
        if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
            response['output'] = 'OK'
            cmd = "cd .. && sudo ./deploy.sh &"
            execute_os_cmd(cmd, sys=True)
        else:
            response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 25)
            if self.session.get('role') == 'USER':
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 26)
        set_api_response(response, self.response)

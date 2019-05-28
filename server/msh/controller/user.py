from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from datetime import datetime
from module import XmlReader, DbManager


class User(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        if self.session.get('user') is not None:
            response = {}
            try:
                data = loads(body)
                username = data['username']
                password = data['password']
                role = data['role']
                tipo_operazione = data['tipo_operazione']
                DbManager()
                if tipo_operazione == "list":
                    response['users'] = DbManager.select_tb_user()
                if tipo_operazione == "update":
                    DbManager.update_tb_user(username, password, role)
                if tipo_operazione == "delete":
                    DbManager.delete_tb_user(username)
                if tipo_operazione == "add":
                    DbManager.insert_tb_user(username, password, role)
                DbManager.close_db()
                response['output'] = 'OK'
            except Exception as e:
                exception("Exception")
                response['output'] = str(e)
            finally:
                response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
                self.response.headers.add('Access-Control-Allow-Origin', '*')
                self.response.headers.add('Content-Type', 'application/json')
                self.response.write(dumps(response, indent=4, sort_keys=True))
                info("RESPONSE CODE: %s", self.response.status)
                info("RESPONSE PAYLOAD: %s", response)
        else:
            self.redirect('/static/page/login.html')
            info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])
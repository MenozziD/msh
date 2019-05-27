from logging import info, exception
from datetime import datetime
from json import dumps, loads
from module import XmlReader
from module import DbManager
from controller import BaseHandler


class Login(BaseHandler):
    def post(self):
        if self.session.get('user'):
            self.session.clear()
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            data = loads(body)
            username = data['user']
            password = data['password']
            DbManager()
            user = DbManager.select_tb_user_from_username(username)
            if len(user) == 1:
                if password == user[0]['password']:
                    self.session['user'] = username
                    response['output'] = 'OK'
                else:
                    response['output'] = 'Password errata'
            else:
                response['output'] = 'Username non trovato'
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
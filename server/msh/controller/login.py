from logging import info, exception
from datetime import datetime
from json import dumps, loads
from module import XmlReader, DbManager
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
            DbManager()
            response = Login.check_user(data)
            if response['output'] == 'OK':
                response = Login.check_password(data)
                if response['output'] == 'OK':
                    username = data['user']
                    user = DbManager.select_tb_user(username)[0]
                    self.session['user'] = username
                    self.session['role'] = user["role"]
                    response['output'] = 'OK'
            DbManager.close_db()
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

    @staticmethod
    def check_user(data):
        response = {}
        user_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'user' in data and data['user'] in user_list:
            response['output'] = 'OK'
        else:
            if 'user' in data:
                response['output'] = "Username non trovato"
            else:
                response['output'] = "Il campo user è obbligatorio"
        return response

    @staticmethod
    def check_password(data):
        response = {}
        user = DbManager.select_tb_user(data['user'])[0]
        if 'password' in data and data['password'] == user['password']:
            response['output'] = 'OK'
        else:
            if 'password' in data:
                response['output'] = "Password errata"
            else:
                response['output'] = "Il campo password è obbligatorio"
        return response


class Logout(BaseHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        self.session.clear()
        response = {
            'output': 'OK',
            'timestamp': datetime.now().strftime(XmlReader.settings['timestamp'])
        }
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(response, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", response)

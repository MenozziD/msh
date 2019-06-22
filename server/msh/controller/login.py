from logging import info, exception
from json import loads
from module import DbManager, set_api_response
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
            DbManager()
            response = Login.check(body)
            if response['output'] == 'OK':
                data = loads(body)
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
            set_api_response(response, self.response)

    @staticmethod
    def check(body):
        response = {}
        if body != "" and Login.validate_format(body):
            data = loads(body)
            response = Login.check_user(data)
            if response['output'] == 'OK':
                response = Login.check_password(data)
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
        return response

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

    @staticmethod
    def validate_format(body):
        try:
            loads(body)
        except ValueError:
            return False
        return True


class Logout(BaseHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        self.session.clear()
        response = {'output': 'OK'}
        set_api_response(response, self.response)

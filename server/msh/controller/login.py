from logging import info, exception
from module import DbManager, set_api_response, validate_format, get_string
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
            response = Login.check(self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                username = data['user']
                user = DbManager.select_tb_user(username)[0]
                self.session['user'] = username
                self.session['role'] = user["role"]
                response['output'] = 'OK'
            else:
                raise Exception(response['output'])
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            set_api_response(response, self.response)

    @staticmethod
    def check(request, body):
        response = {}
        if body != "" and validate_format(request):
            data = request.json
            response = Login.check_user(data)
            if response['output'] == 'OK':
                response = Login.check_password(data)
        else:
            if body != "":
                response['output'] = get_string(22)
            else:
                response['output'] = get_string(21)
        return response

    @staticmethod
    def check_user(data):
        response = {}
        user_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'user' in data and data['user'] in user_list:
            response['output'] = 'OK'
        else:
            if 'user' in data:
                response['output'] = get_string(36)
            else:
                response['output'] = get_string(23, da_sostiuire="user")
        return response

    @staticmethod
    def check_password(data):
        response = {}
        user = DbManager.select_tb_user(data['user'])[0]
        if 'password' in data and data['password'] == user['password']:
            response['output'] = 'OK'
        else:
            if 'password' in data:
                response['output'] = get_string(37)
            else:
                response['output'] = get_string(23, da_sostiuire="password")
        return response


class Logout(BaseHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        self.session.clear()
        response = {'output': 'OK'}
        set_api_response(response, self.response)

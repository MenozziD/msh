from controller import BaseHandler
from logging import info, exception
from module import DbManager, add_user, delete_user, update_user, set_api_response, validate_format, get_string


class User(BaseHandler):

    tipo_operazione = ['list', 'update', 'delete', 'add']
    campi_aggiornabili = ['role', 'password']

    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            DbManager()
            response = User.check(self.session.get('user'), self.session.get('role'), self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                tipo_operazione = data['tipo_operazione']
                username = None
                password = None
                role = None
                if 'username' in data:
                    username = data['username']
                if 'password' in data:
                    password = data['password']
                if 'role' in data:
                    role = data['role']
                funzioni = {
                    'list': User.user_list,
                    'update': User.user_update,
                    'delete': User.user_delete,
                    'add': User.user_add
                }
                parametri = {
                    'list': [self.session.get('user'), self.session.get('role')],
                    'update': [username, password, role],
                    'delete': [username],
                    'add': [username, password, role]
                }
                response = funzioni[tipo_operazione](*parametri[tipo_operazione])
            else:
                raise Exception(response['output'])
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            set_api_response(response, self.response)

    @staticmethod
    def check(user, role, request, body):
        response = {}
        if body != "" and validate_format(request):
            data = request.json
            if 'tipo_operazione' in data and data['tipo_operazione'] in User.tipo_operazione:
                response = User.check_user(user, role, data['tipo_operazione'])
                response = User.check_operation_param(response, data, user, role)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = get_string(24, da_sostiuire="tipo_operazione", da_aggiungere=', '.join(User.tipo_operazione))
                else:
                    response['output'] = get_string(23, da_sostiuire="tipo_operazione")
        else:
            if body != "":
                response['output'] = get_string(22)
            else:
                response['output'] = get_string(21)
        return response

    @staticmethod
    def check_operation_param(response, data, user, role):
        if response['output'] == 'OK':
            if data['tipo_operazione'] == 'delete':
                response = User.check_username_exist(data)
                if response['output'] == 'OK':
                    response = User.check_one_admin(data)
            if data['tipo_operazione'] == 'add':
                response = User.check_add(data)
            if data['tipo_operazione'] == 'update':
                response = User.check_update(data, user, role)
        return response

    @staticmethod
    def check_add(data):
        response = User.check_username_not_exist(data)
        if response['output'] == 'OK':
            response = User.check_role(data)
            if response['output'] == 'OK':
                response = User.check_password(data)
        return response

    @staticmethod
    def check_update(data, user, role):
        response = User.check_username_exist(data)
        if response['output'] == 'OK':
            response = User.check_any_to_update(data)
            if response['output'] == 'OK':
                response = User.check_role(data, required=False, to_modify=True, session_role=role)
                if response['output'] == 'OK':
                    response = User.check_password(data, required=False, to_modify=True, session_user=user)
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('add', 'delete'):
                if role != 'ADMIN':
                    response['output'] = get_string(26)
                else:
                    response['output'] = 'OK'
            else:
                response['output'] = 'OK'
        else:
            response['output'] = get_string(25)
        return response

    @staticmethod
    def check_username_exist(data):
        response = {}
        username_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'username' in data and data['username'] in username_list:
            response['output'] = 'OK'
        else:
            if 'username' in data:
                response['output'] = get_string(24, da_sostiuire="username", da_aggiungere=', '.join(username_list))
            else:
                response['output'] = get_string(27, da_aggiungere="username")
        return response

    @staticmethod
    def check_username_not_exist(data):
        response = {}
        username_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'username' in data and data['username'] not in username_list:
            response['output'] = 'OK'
        else:
            if 'username' in data:
                response['output'] = get_string(28)
            else:
                response['output'] = get_string(27, da_aggiungere="username")
        return response

    @staticmethod
    def check_one_admin(data, to_modify=False):
        response = {}
        to_delete = DbManager.select_tb_user(data['username'])[0]
        role_list = [d['role'] for d in DbManager.select_tb_user()]
        admin = 0
        for role in role_list:
            if role == 'ADMIN':
                admin = admin + 1
        if to_delete['role'] == 'ADMIN' and admin == 1 and ((not to_modify) or (to_modify and to_delete['role'] != data['role'])):
            response['output'] = get_string(29)
        else:
            response['output'] = 'OK'
        return response

    @staticmethod
    def check_role(data, required=True, to_modify=False, session_role=''):
        response = {}
        role_list = {'USER', 'ADMIN'}
        if 'role' in data and data['role'] in role_list:
            response['output'] = 'OK'
            if to_modify:
                response = User.check_user_for_role(data, session_role)
        else:
            if 'role' in data:
                response['output'] = get_string(24, da_sostiuire="role", da_aggiungere=', '.join(role_list))
            else:
                if required:
                    response['output'] = get_string(27, da_aggiungere="role")
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def check_user_for_role(data, session_role):
        response = {}
        if session_role == 'ADMIN':
            response = User.check_one_admin(data, to_modify=True)
        else:
            response['output'] = get_string(30)
        return response

    @staticmethod
    def check_password(data, required=True, to_modify=False, session_user=''):
        response = {}
        if 'password' in data and len(data['password']) >= 4:
            response['output'] = 'OK'
            if to_modify:
                response = User.check_user_for_password(data, session_user)
        else:
            if 'password' in data:
                response['output'] = get_string(31)
            else:
                if required:
                    response['output'] = get_string(27, da_aggiungere="password")
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def check_user_for_password(data, session_user):
        response = {}
        if session_user == data['username']:
            response['output'] = 'OK'
        else:
            response['output'] = get_string(32)
        return response

    @staticmethod
    def check_any_to_update(data):
        response = {}
        if 'role' in data or 'password' in data:
            response['output'] = 'OK'
        else:
            response['output'] = get_string(33, da_aggiungere=', '.join(User.campi_aggiornabili))
        return response

    @staticmethod
    def user_list(session_user, session_role):
        if session_role == 'ADMIN':
            users = DbManager.select_tb_user()
            for user in users:
                if user['username'] != session_user:
                    user['password'] = ''
        else:
            users = DbManager.select_tb_user(session_user)
        response = {
            'users': users,
            'user_role': session_role,
            'user_username': session_user,
            'output': 'OK'
        }
        return response

    @staticmethod
    def user_delete(username):
        DbManager.delete_tb_user(username)
        delete_user(username)
        response = {'output': 'OK'}
        return response

    @staticmethod
    def user_add(username, password, role):
        DbManager.insert_tb_user(username, password, role)
        add_user(username, password)
        response = {'output': 'OK'}
        return response

    @staticmethod
    def user_update(username, password, role):
        DbManager.update_tb_user(username, password, role)
        if password is not None:
            update_user(username, password)
        response = {'output': 'OK'}
        return response

from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from datetime import datetime
from module import XmlReader, DbManager, add_user, delete_user, update_user


class User(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            DbManager()
            response = User.check(self.session.get('user'), self.session.get('role'), body)
            if response['output'] == 'OK':
                data = loads(body)
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
    def check(user, role, body):
        response = {}
        if body != "" and User.validate_format(body):
            data = loads(body)
            if 'tipo_operazione' in data and data['tipo_operazione'] in ('list', 'update', 'delete', 'add'):
                response = User.check_user(user, role, data['tipo_operazione'])
                if response['output'] == 'OK':
                    if data['tipo_operazione'] == 'delete':
                        response = User.check_username_exist(data)
                        if response['output'] == 'OK':
                            response = User.check_one_admin(data)
                    if data['tipo_operazione'] == 'add':
                        response = User.check_username_not_exist(data)
                        if response['output'] == 'OK':
                            response = User.check_role(data)
                            if response['output'] == 'OK':
                                response = User.check_password(data)
                    if data['tipo_operazione'] == 'update':
                        response = User.check_username_exist(data)
                        if response['output'] == 'OK':
                            response = User.check_role(data, required=False, to_modify=True, session_role=role)
                            if response['output'] == 'OK':
                                response = User.check_password(data, required=False, to_modify=True, session_user=user)
            else:
                if 'tipo_operazione' in data:
                    response['output'] = 'Il campo tipo_operazione deve assumere uno dei seguenti valori: list, update, delete, add'
                else:
                    response['output'] = 'Il campo tipo_operazione è obbligatorio'
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
        return response

    @staticmethod
    def check_user(user, role, tipo_operazione):
        response = {}
        if user is not None:
            if tipo_operazione in ('add', 'delete'):
                if role != 'ADMIN':
                    response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
                else:
                    response['output'] = 'OK'
            else:
                response['output'] = 'OK'
        else:
            response['output'] = 'Devi effettuare la login per utilizzare questa API'
        return response

    @staticmethod
    def check_username_exist(data):
        response = {}
        username_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'username' in data and data['username'] in username_list:
            response['output'] = 'OK'
        else:
            if 'username' in data:
                response['output'] = "Il campo username deve assumere uno dei seguenti valori: " + ', '.join(username_list)
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo username"
        return response

    @staticmethod
    def check_username_not_exist(data):
        response = {}
        username_list = [d['username'] for d in DbManager.select_tb_user()]
        if 'username' in data and data['username'] not in username_list:
            response['output'] = 'OK'
        else:
            if 'username' in data:
                response['output'] = "Esiste già un utente con questo nome"
            else:
                response['output'] = "Per l'operazione scelta è obbligatorio il campo username"
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
            response['output'] = 'Deve essere sempre presente almeno un utente ADMIN'
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
                to_update = DbManager.select_tb_user(data['username'])[0]
                if to_update['role'] != data['role'] and session_role == 'ADMIN':
                    User.check_one_admin(data, to_modify=True)
                else:
                    if session_role != 'ADMIN':
                        response['output'] = 'Solo gli ADMIN possono modificare i ruoli'
        else:
            if 'role' in data:
                response['output'] = "Il campo role deve assumere uno dei seguenti valori: " + ', '.join(role_list)
            else:
                if required:
                    response['output'] = "Per l'operazione scelta è obbligatorio il campo role"
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def check_password(data, required=True, to_modify=False, session_user=''):
        response = {}
        if 'password' in data and len(data['password']) >= 4:
            response['output'] = 'OK'
            if to_modify:
                to_update = DbManager.select_tb_user(data['username'])[0]
                if to_update['password'] != data['password']:
                    if session_user == data['username']:
                        response['output'] = 'OK'
                    else:
                        response['output'] = 'Solo l\'utente propietario può modificare la sua password'
        else:
            if 'password' in data:
                response['output'] = "Il campo password deve avere una lunghezza di almeno 4 caratteri"
            else:
                if required:
                    response['output'] = "Per l'operazione scelta è obbligatorio il campo password"
                else:
                    response['output'] = 'OK'
        return response

    @staticmethod
    def validate_format(body):
        try:
            loads(body)
        except ValueError:
            return False
        return True

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

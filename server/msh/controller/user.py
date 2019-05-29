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
        if self.session.get('user') is not None:
            response = {}
            try:
                data = loads(body)
                username = data['username']
                password = data['password']
                role = data['role']
                tipo_operazione = data['tipo_operazione']
                if self.session.get('role') == 'ADMIN' or tipo_operazione == 'update' or tipo_operazione == 'list':
                    DbManager()
                    if tipo_operazione == "list":
                        if self.session.get('role') == 'ADMIN':
                            response['users'] = DbManager.select_tb_user()
                        else:
                            response['users'] = DbManager.select_tb_user(self.session.get('user'))
                        response['output'] = 'OK'
                    if tipo_operazione == "update":
                        to_update = DbManager.select_tb_user(username)[0]
                        if to_update['role'] != role:
                            if self.session.get('role') == 'ADMIN':
                                if to_update['password'] != password:
                                    if self.session.get('user') == username:
                                        DbManager.update_tb_user(username, password, role)
                                        update_user(username, password)
                                        response['output'] = 'OK'
                                    else:
                                        response['output'] = 'Solo l\'utente propietario può modificare la sua password'
                                else:
                                    DbManager.update_tb_user(username, password, role)
                                    update_user(username, password)
                                    response['output'] = 'OK'
                            else:
                                response['output'] = 'Solo gli ADMIN possono modificare i ruoli'
                        else:
                            if to_update['password'] != password:
                                if self.session.get('user') == username:
                                    DbManager.update_tb_user(username, password, role)
                                    update_user(username, password)
                                    response['output'] = 'OK'
                                else:
                                    response['output'] = 'Solo l\'utente propietario può modificare la sua password'
                    if tipo_operazione == "delete":
                        users = DbManager.select_tb_user()
                        to_delete = DbManager.select_tb_user(username)[0]
                        admin = 0
                        for user in users:
                            if user['role'] == 'ADMIN':
                                admin = admin + 1
                        if to_delete['role'] == 'ADMIN' and admin == 1:
                            response['output'] = 'Deve essere sempre presente almeno un utente ADMIN'
                        else:
                            DbManager.delete_tb_user(username)
                            delete_user(username)
                            response['output'] = 'OK'
                    if tipo_operazione == "add":
                        users = DbManager.select_tb_user(username)
                        if len(users) == 0:
                            DbManager.insert_tb_user(username, password, role)
                            add_user(username, password)
                            response['output'] = 'OK'
                        else:
                            response['output'] = 'Username già utilizzato'
                    DbManager.close_db()
                else:
                    response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
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

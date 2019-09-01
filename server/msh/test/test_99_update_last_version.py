from msh import Msh
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_user, simulate_login_admin, read_xml


class TestUpdateLastVersion(TestCase):

    def test_not_logged(self):
        read_xml()
        request = Request.blank('/api/update_last_version')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Devi effettuare la login per utilizzare questa API')

    def test_logged_not_admin(self):
        read_xml()
        request = Request.blank('/api/update_last_version')
        request.method = 'GET'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'La funzione richiesta può essere eseguita solo da un ADMIN')

    def test_logged_admin(self):
        read_xml()
        request = Request.blank('/api/update_last_version')
        request.method = 'GET'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

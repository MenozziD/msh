from msh import Msh
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_user, read_xml


class TestLogin(TestCase):

    def test_get(self):
        request = Request.blank('/api/login')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 405)

    def test_no_payload(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_payload_empty(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.body = b'{}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo user è obbligatorio')

    def test_payload_with_user_not_exist(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "user":"xyz"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Username non trovato')

    def test_payload_with_user_exist_without_password(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "user":"test"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo password è obbligatorio')

    def test_payload_with_user_exists_and_password_not_correct(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "user":"test",' \
                       b'   "password":"fdgdf"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Password errata')

    def test_payload_with_user_exists_and_password_correct(self):
        read_xml()
        request = Request.blank('/api/login')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "user":"test",' \
                       b'   "password":"test"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_logout(self):
        read_xml()
        request = Request.blank('/logout')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

from msh import app
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_admin, simulate_login_user, read_xml


class TestUploadArduino(TestCase):

    def test_no_payload(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_payload_empty(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.body = b'{}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo tipo_operazione è obbligatorio')

    def test_payload_with_operazione_not_exist(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"dsgsd"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo tipo_operazione deve assumere uno dei seguenti valori: upload, core, tipo')

    def test_payload_with_operazione_exist_not_logged(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"tipo"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Devi effettuare la login per utilizzare questa API')

    def test_payload_with_operazione_tipo_logged(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"tipo"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_core_logged(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"core"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_upload_logged_user(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'La funzione richiesta può essere eseguita solo da un ADMIN')

    def test_payload_with_operazione_upload_without_core_logged_admin(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo core')

    def test_payload_with_operazione_upload_with_core_not_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload",' \
                       b'   "core":"afdasf"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find("Il campo core deve assumere uno dei seguenti valori:"), 0)

    def test_payload_with_operazione_upload_with_core_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload",' \
                       b'   "core":"Generic ESP8266 Module"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo tipologia')

    def test_payload_with_operazione_upload_with_core_exist_tipologia_not_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload",' \
                       b'   "core":"Generic ESP8266 Module",' \
                       b'   "tipologia":"fdsfs"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find("Il campo tipologia deve assumere uno dei seguenti valori:"), 0)

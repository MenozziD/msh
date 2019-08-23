from msh import app
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_admin, simulate_login_user, read_xml, simulate_os_command, simulate_request_http
from module import upload_arduino, DbManager


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
        self.assertEqual(response.json['output'].find('Il campo tipo_operazione deve assumere uno dei seguenti valori:'), 0)

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
        simulate_request_http("tipologia_script_arduino")
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
        simulate_os_command("arduino-cli-board-listall")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"core"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_compile_logged_user(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'La funzione richiesta può essere eseguita solo da un ADMIN')

    def test_payload_with_operazione_compile_without_core_logged_admin(self):
        read_xml()
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo core')

    def test_payload_with_operazione_compile_with_core_not_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-board-listall")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile",' \
                       b'   "core":"afdasf"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find("Il campo core deve assumere uno dei seguenti valori:"), 0)

    def test_payload_with_operazione_compile_with_core_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-board-listall")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile",' \
                       b'   "core":"Generic ESP8266 Module"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo tipologia')

    def test_payload_with_operazione_compile_with_core_exist_tipologia_not_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-board-listall")
        simulate_request_http("tipologia_script_arduino")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile",' \
                       b'   "core":"Generic ESP8266 Module",' \
                       b'   "tipologia":"fdsfs"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find("Il campo tipologia deve assumere uno dei seguenti valori:"), 0)

    def test_payload_with_operazione_compile_ok_with_core_exist_tipologia_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-compile-ok")
        simulate_request_http("tipologia_script_arduino")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile",' \
                       b'   "core":"core_test",' \
                       b'   "tipologia":"DEV_1"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_compile_ko_with_core_exist_tipologia_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-compile-ko")
        simulate_request_http("tipologia_script_arduino")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"compile",' \
                       b'   "core":"core_test",' \
                       b'   "tipologia":"DEV_1"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Errore compilazione')

    def test_payload_with_operazione_upload_ok_with_core_exist_tipologia_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-upload-ok")
        simulate_request_http("tipologia_script_arduino")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload",' \
                       b'   "core":"core_test",' \
                       b'   "tipologia":"DEV_1"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_upload_ko_with_core_exist_tipologia_exist_logged_admin(self):
        read_xml()
        simulate_os_command("arduino-cli-upload-ko")
        simulate_request_http("tipologia_script_arduino")
        request = Request.blank('/api/upload_arduino')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"upload",' \
                       b'   "core":"core_test",' \
                       b'   "tipologia":"DEV_1"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Errore upload')

    def test_upload_arduino_no_usb(self):
        read_xml()
        DbManager()
        simulate_os_command("no-usb")
        response = upload_arduino('core', 'tipologia')
        self.assertEqual(response['output'], 'Nessun dispositivo collegato')
        DbManager().close_db()

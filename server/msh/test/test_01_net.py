from msh import app
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_admin, read_xml, simulate_os_command


class TestNet(TestCase):

    def test_no_payload(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_payload_empty(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.body = b'{}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo tipo_operazione è obbligatorio')

    def test_payload_with_operazione_not_exist(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"dsgsd"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo tipo_operazione deve assumere uno dei seguenti valori: scan, list, type, command, update, delete, cmd')

    def test_payload_with_operazione_exist_not_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"list"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Devi effettuare la login per utilizzare questa API')

    def test_payload_with_operazione_list_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"list"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_type_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"type"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_scan_ok_logged(self):
        read_xml()
        simulate_os_command("scan-ok")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"scan"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_scan_ko_logged(self):
        read_xml()
        simulate_os_command("scan-ko")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"scan"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_command_without_type_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"command"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo tipo')

    def test_payload_with_operazione_command_and_type_not_exist_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"command",' \
                       b'   "tipo":"dfsf"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo tipo deve assumere uno dei seguenti valori'), 0)

    def test_payload_with_operazione_command_and_type_exist_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"command",' \
                       b'   "tipo":"NET"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

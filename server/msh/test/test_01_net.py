from msh import app
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_admin, read_xml, simulate_os_command, simulate_login_user


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

    def test_payload_with_operazione_list_logged_admin(self):
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

    def test_payload_with_operazione_list_logged_user(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
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
        self.assertEqual(response.json['output'], 'Errore netscan')

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

    def test_payload_with_operazione_delete_logged_user(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'La funzione richiesta può essere eseguita solo da un ADMIN')

    def test_payload_with_operazione_delete_without_mac_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo mac')

    def test_payload_with_operazione_delete_mac_not_exists_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete",' \
                       b'   "mac":"FF:FF:FF:FF:FF:FF"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo mac deve assumere uno dei seguenti valori: '), 0)

    def test_payload_with_operazione_delete_mac_exists_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete",' \
                       b'   "mac":"EE:FF:AA:BB:00:33"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_update_no_data_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "mac":"A1:FF:AA:BB:00:33"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Nessun campo da aggiornare, i possibili campi da aggiornare sono codice, tipo, user, password')

    def test_payload_with_operazione_update_user_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "mac":"A1:FF:AA:BB:00:33",' \
                       b'   "user":"test",' \
                       b'   "password":"test"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_update_code_empty_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "mac":"A1:FF:AA:BB:00:33",' \
                       b'   "codice":""' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo codice non può essere valorizzato con una stringa vuota')

    def test_payload_with_operazione_update_code_duplicate_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "mac":"A1:FF:AA:BB:00:33",' \
                       b'   "codice":"device_test_duplicato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Esiste già un dispositivo con questo codice')

    def test_payload_with_operazione_update_code_ok_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "mac":"A1:FF:AA:BB:00:33",' \
                       b'   "codice":"device_test_rinominato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_with_operazione_cmd_without_dispositivo_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo dispositivo')

    def test_payload_with_operazione_cmd_dispositivo_not_exists_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"dfsf"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo dispositivo deve assumere uno dei seguenti valori: '), 0)

    def test_payload_with_operazione_cmd_dispositivo_exists_without_comando_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_duplicato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo comando')

    def test_payload_with_operazione_cmd_dispositivo_exists_comando_not_exists_logged(self):
        read_xml()
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_duplicato",' \
                       b'   "comando":"fasdfs"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo comando deve assumere uno dei seguenti valori: '), 0)

    def test_payload_with_operazione_cmd_ping_ok_logged(self):
        read_xml()
        simulate_os_command("ping-ok")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_duplicato",' \
                       b'   "comando":"stato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_ping_fail_logged(self):
        read_xml()
        simulate_os_command("ping-fail")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_duplicato",' \
                       b'   "comando":"stato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_ping_ko_logged(self):
        read_xml()
        simulate_os_command("ping-ko")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_duplicato",' \
                       b'   "comando":"stato"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "Errore ping")

    def test_payload_with_operazione_cmd_pcwin_on_ok_logged(self):
        read_xml()
        simulate_os_command("pcwin-on-ok")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"on"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_pcwin_on_fail_logged(self):
        read_xml()
        simulate_os_command("pcwin-on-fail")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"on"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_pcwin_on_ko_logged(self):
        read_xml()
        simulate_os_command("pcwin-on-ko")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"on"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "Errore pcwin on")

    def test_payload_with_operazione_cmd_pcwin_off_ok_logged(self):
        read_xml()
        simulate_os_command("pcwin-off-ok")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"off"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_pcwin_off_fail_logged(self):
        read_xml()
        simulate_os_command("pcwin-off-fail")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"off"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "OK")

    def test_payload_with_operazione_cmd_pcwin_off_ko_logged(self):
        read_xml()
        simulate_os_command("pcwin-off-ko")
        request = Request.blank('/api/net')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"cmd",' \
                       b'   "dispositivo":"device_test_pc_win",' \
                       b'   "comando":"off"' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], "Errore pcwin off")

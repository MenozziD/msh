from msh import Msh
from unittest import TestCase
from webapp3 import Request
from test import simulate_login_admin, simulate_login_user, read_xml


class TestUser(TestCase):

    def test_a_no_payload(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_b_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_c_payload_empty(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.body = b'{}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo tipo_operazione è obbligatorio')

    def test_d_payload_with_operazione_not_exist(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"dsgsd"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo tipo_operazione deve assumere uno dei seguenti valori:'), 0)

    def test_e_payload_with_operazione_exist_not_logged(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "tipo_operazione":"list"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Devi effettuare la login per utilizzare questa API')

    def test_f_payload_with_operazione_list_logged(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"list"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_g_payload_with_operazione_add_logged_user(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'La funzione richiesta può essere eseguita solo da un ADMIN')

    def test_h_payload_with_operazione_add_without_username_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo username')

    def test_i_payload_with_operazione_add_with_username_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"test"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Esiste già un utente con questo nome')

    def test_l_payload_with_operazione_add_with_username_not_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"to_delete"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo role')

    def test_m_payload_with_operazione_add_with_username_not_exist_role_not_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"to_delete",' \
                       b'   "role":"dfsf"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find("Il campo role deve assumere uno dei seguenti valori:"), 0)

    def test_n_payload_with_operazione_add_with_username_not_exist_role_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"to_delete",' \
                       b'   "role":"USER"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo password')

    def test_o_payload_with_operazione_add_with_username_not_exist_role_exist_password_min_four_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"to_delete",' \
                       b'   "role":"USER",' \
                       b'   "password":"ss"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il campo password deve avere una lunghezza di almeno 4 caratteri')

    def test_p_payload_with_operazione_add_with_username_not_exist_role_exist_password_max_four_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"add",' \
                       b'   "username":"to_delete",' \
                       b'   "role":"USER",' \
                       b'   "password":"to_delete"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_q_payload_with_operazione_delete_without_username_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Per l\'operazione scelta è obbligatorio il campo username')

    def test_r_payload_with_operazione_delete_with_username_not_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete",' \
                       b'   "username":"dfsfs"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Il campo username deve assumere uno dei seguenti valori:'), 0)

    def test_s_payload_with_operazione_delete_with_username_exist_last_admin_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete",' \
                       b'   "username":"admin"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Deve essere sempre presente almeno un utente ADMIN')

    def test_t_payload_with_operazione_delete_with_username_exist_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"delete",' \
                       b'   "username":"to_delete"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_u_payload_with_operazione_update_with_username_exist_no_data_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"test"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'].find('Nessun campo da aggiornare, i possibili campi da aggiornare sono'), 0)

    def test_v_payload_with_operazione_update_with_username_exist_with_data_logged_user(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"test",' \
                       b'   "role":"ADMIN"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Solo gli ADMIN possono modificare i ruoli')

    def test_z_payload_with_operazione_update_with_username_exist_with_data_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"test",' \
                       b'   "role":"ADMIN"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"test",' \
                       b'   "role":"USER"' \
                       b'}'
        request.get_response(Msh.app)

    def test_za_payload_with_operazione_update_password_ko_with_username_exist_with_data_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"test",' \
                       b'   "password":"test1"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Solo l\'utente propietario può modificare la sua password')

    def test_zb_payload_with_operazione_update_password_ok_with_username_exist_with_data_logged_admin(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"admin",' \
                       b'   "password":"admin1"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')
        request.body = b'{' \
                       b'   "tipo_operazione":"update",' \
                       b'   "username":"admin",' \
                       b'   "password":"admin"' \
                       b'}'
        request.get_response(Msh.app)

    def test_zc_payload_with_operazione_list_logged_user(self):
        read_xml()
        request = Request.blank('/api/user')
        request.method = 'POST'
        request.headers['Cookie'] = simulate_login_user().headers['Set-Cookie']
        request.body = b'{' \
                       b'   "tipo_operazione":"list"' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')



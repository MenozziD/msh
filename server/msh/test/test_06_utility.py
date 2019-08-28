from unittest import TestCase
from test import read_xml_prod, read_xml, simulate_os_command
from module import execute_os_cmd, execute_ssh_cmd, execute_request_http, check_server_connection, DbManager


class TestUtility(TestCase):

    def test_execute_os_cmd_run(self):
        read_xml_prod()
        response = execute_os_cmd("pwd")
        self.assertEqual(response['return_code'], 0)
        self.assertNotEqual(response['cmd_out'], "")

    def test_execute_os_cmd_run_ko(self):
        read_xml_prod()
        response = execute_os_cmd("sudo arduino-cli board details sdad")
        self.assertNotEqual(response['return_code'], 0)
        self.assertNotEqual(response['cmd_err'], "")

    def test_execute_os_cmd_check_output(self):
        read_xml_prod()
        response = execute_os_cmd("pwd", check_out=True)
        self.assertNotEqual(response['cmd_out'], "")

    def test_execute_os_cmd_system(self):
        read_xml_prod()
        response = execute_os_cmd("pwd", sys=True)
        self.assertEqual(response, {})

    def test_execute_os_cmd_system_exception(self):
        read_xml_prod()
        response = execute_os_cmd("afasf", sys=True)
        self.assertEqual(response['return_code'], -1)
        self.assertNotEqual(response['cmd_err'], "")

    def test_execute_ssh_cmd_ko_login(self):
        read_xml_prod()
        DbManager()
        response = execute_ssh_cmd('127.0.0.1', 'test_user', 'test1234', 'pwd')
        self.assertEqual(response['output'], 'Credenzilai non valide')
        DbManager.close_db()

    def test_execute_ssh_cmd_ko_other(self):
        read_xml_prod()
        response = execute_ssh_cmd('noip', 'test_user', 'test1234', 'pwd')
        self.assertNotEqual(response['output'], "OK")

    def test_execute_ssh_cmd_ok(self):
        read_xml_prod()
        response = execute_ssh_cmd('127.0.0.1', 'test_user', 'test_password', 'pwd')
        self.assertEqual(response['output'], "OK")

    def test_execute_request_http(self):
        read_xml_prod()
        response = execute_request_http("https://api.macvendors.com/5C:6A:80:EB:31:17")
        self.assertNotEqual(response, "")

    def test_check_server_connection_ok(self):
        read_xml()
        simulate_os_command('internet-ok')
        self.assertEqual(check_server_connection("url", 1, 1), True)
    
    def test_check_server_connection_timeout(self):
        read_xml()
        simulate_os_command('internet-timeout')
        self.assertEqual(check_server_connection("url", 1, 1), False)

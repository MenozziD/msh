from unittest import TestCase
from test import simulate_os_command, read_xml
from msh import Msh


class TestMsh(TestCase):

    def test_a_oauth_serveo_no_internet(self):
        simulate_os_command("internet-timeout")
        Msh("settings_test.xml")
        self.assertEqual(len(Msh.service_avaiable), 0)

    def test_b_oauth_serveo(self):
        simulate_os_command("internet-ok")
        Msh("settings_test.xml")
        self.assertEqual(len(Msh.service_avaiable), 2)

    def test_check_server_connection_no_timeout(self):
        simulate_os_command("no-usb")
        self.assertEqual(Msh.check_server_connection("url", 1, 1), False)

    def test_check_serveo_ko(self):
        read_xml()
        simulate_os_command("internet-timeout")
        self.assertEqual(Msh.final_check('serveo', 'dominio')[0], True)

from unittest import TestCase
from test import simulate_os_command, read_xml
from msh import main, check_server_connection, start_serveo


class TestMsh(TestCase):

    def test_oauth_serveo(self):
        simulate_os_command("internet-ok")
        self.assertEqual(main("settings_test.xml"), True)

    def test_check_server_connection_no_timeout(self):
        simulate_os_command("no-usb")
        self.assertEqual(check_server_connection("url", 1, 1), False)

    def test_check_server_ko(self):
        read_xml()
        simulate_os_command("internet-timeout")
        self.assertEqual(start_serveo(), True)

    def test_oauth_serveo_no_internet(self):
        simulate_os_command("internet-timeout")
        self.assertEqual(main("settings_test.xml"), True)


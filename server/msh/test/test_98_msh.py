from unittest import TestCase
from test import simulate_os_command
from msh import main
from pytest import raises


class TestMsh(TestCase):

    def test_oauth_serveo(self):
        simulate_os_command("oauth-serveo")
        self.assertEqual(main("settings_test.xml"), True)

    def test_oauth_serveo_no_internet(self):
        simulate_os_command("no-usb")
        self.assertEqual(main("settings_test.xml"), True)

    def test_exception(self):
        with raises(FileNotFoundError):
            main("settings_not_found.xml")

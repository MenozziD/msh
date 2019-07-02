from unittest import TestCase
from test import simulate_os_command
from msh import main
from urllib import request
from pytest import raises


class TestMsh(TestCase):

    def test_oauth_serveo(self):
        simulate_os_command("oauth-serveo")
        main("settings_test.xml", "65000")
        url = "http://localhost:65000/static/page/login.html"
        response = request.urlopen(url)
        self.assertEqual(response.getcode(), 200)

    def test_oauth_serveo_no_internet(self):
        simulate_os_command("no-usb")
        main("settings_test.xml", "65000")
        url = "http://localhost:65000/static/page/login.html"
        response = request.urlopen(url)
        self.assertEqual(response.getcode(), 200)

    def test_exception(self):
        with raises(Exception):
            main("settings_not_found.xml", "65000")

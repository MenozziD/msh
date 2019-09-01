from msh import Msh
from unittest import TestCase
from webapp3 import Request
from test import read_xml, simulate_login_admin


class TestStatic(TestCase):

    def test_index(self):
        read_xml()
        request = Request.blank('/')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/static/page/index.html')

    def test_icon(self):
        read_xml()
        request = Request.blank('/favicon.ico')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/static/image/hub.png')

    def test_static_resources_without_login(self):
        read_xml()
        request = Request.blank('/static/page/index.html')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/static/page/login.html')

    def test_login_resources_without_login(self):
        read_xml()
        request = Request.blank('/static/page/login.html')
        request.method = 'GET'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)

    def test_static_resources_with_login(self):
        read_xml()
        request = Request.blank('/static/page/index.html')
        request.method = 'GET'
        request.headers['Cookie'] = simulate_login_admin().headers['Set-Cookie']
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)

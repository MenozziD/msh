from webapp3 import Request
from msh import Msh
from module import XmlReader
from json import load, dump


def simulate_login_admin():
    request = Request.blank('/api/login')
    request.method = 'POST'
    request.body = b'{' \
                   b'   "user":"admin",' \
                   b'   "password":"admin"' \
                   b'}'
    return request.get_response(Msh.app)


def simulate_login_user():
    request = Request.blank('/api/login')
    request.method = 'POST'
    request.body = b'{' \
                   b'   "user":"test",' \
                   b'   "password":"test"' \
                   b'}'
    return request.get_response(Msh.app)


def simulate_os_command(command):
    f = open('mock_so.json')
    data = load(f)
    f.close()
    f = open('command_simulate.json', 'w')
    dump(data[command], f)
    f.close()
    return


def simulate_request_http(url):
    f = open('mock_request.json')
    data = load(f)
    f.close()
    f = open('request_simulate.json', 'w')
    dump(data[url], f)
    f.close()
    return


def read_xml():
    XmlReader("settings_test.xml")


def read_xml_prod():
    XmlReader("settings_test.xml")
    XmlReader.settings['ambiente'] = 'PROD'

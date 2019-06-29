from webapp3 import Request
from msh import app
from module import XmlReader
from os import remove


def simulate_login_admin():
    request = Request.blank('/api/login')
    request.method = 'POST'
    request.body = b'{' \
                   b'   "user":"admin",' \
                   b'   "password":"admin"' \
                   b'}'
    return request.get_response(app)


def simulate_login_user():
    request = Request.blank('/api/login')
    request.method = 'POST'
    request.body = b'{' \
                   b'   "user":"test",' \
                   b'   "password":"test"' \
                   b'}'
    return request.get_response(app)


def read_xml():
    f = open("settings_log_console.xml", "w")
    f.write("<settings>"
            "   <lingua>IT</lingua>"
            "   <path_db>db/test.db</path_db>"
            "   <path_datastore>../oauth/datastore_test.js</path_datastore>"
            "   <timestamp>%Y-%m-%d %H:%M:%S</timestamp>"
            "   <project_id_google_actions>fake_project</project_id_google_actions>"
            "   <subdomain_oauth>fake_oauth</subdomain_oauth>"
            "   <subdomain_webapp>fake_webapp</subdomain_webapp>"
            "   <log>"
            "       <!-- Se valorizzato con None logga in console -->"
            "       <filename>None</filename>"
            "       <format>%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s</format>"
            "       <!-- debug, info, warning, error, critical -->"
            "       <level>info</level>"
            "   </log>"
            "</settings>")
    f.close()
    XmlReader("settings_log_console.xml")
    remove("settings_log_console.xml")

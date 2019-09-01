from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module import XmlReader, execute_os_cmd, get_gateway
from controller import handle_error
from string import ascii_letters, digits
from random import choice
from netifaces import AF_INET, ifaddresses
from time import sleep


class Msh:
    config = {
        'webapp3_extras.sessions': {
            'secret_key': ''.join(choice(ascii_letters + digits) for _ in range(36))
        }
    }
    app = WSGIApplication([
        ('/api/net', 'controller.Net'),
        ('/api/home', 'controller.Home'),
        ('/api/login', 'controller.Login'),
        ('/api/user', 'controller.User'),
        ('/api/upload_arduino', 'controller.UploadArduino'),
        ('/api/update_last_version', 'controller.UpdateLastVersion'),
        ('/logout', 'controller.Logout'),
        ('/favicon.ico', 'controller.Icon'),
        ('/', 'controller.Index'),
        (r'/static/(\D+)', 'controller.Static'),
    ], config=config, debug=True)
    app.error_handlers[404] = handle_error
    app.error_handlers[405] = handle_error
    app.error_handlers[500] = handle_error
    service_avaiable = []
    oauth_urls = []
    webapp_urls = []

    def __init__(self, settings_path):
        XmlReader(settings_path)
        basicConfig(
            filename=XmlReader.settings['log']['filename'],
            format=XmlReader.settings['log']['format'],
            level=XmlReader.settings['log']['level'])
        porta = '65177'
        Msh.start_oauth()
        if Msh.check_server_connection("http://www.google.com", 10, 5):
            Msh.start_dns_service("http://serveo.net", Msh.start_serveo, "serveo")
            Msh.start_dns_service("http://pagekite.net", Msh.start_pagekite, "pagekite")
        if len(Msh.service_avaiable) == 0:
            info("Avvio solo in locale")
            execute_os_cmd("sudo service serveo stop")
            ip_address = ifaddresses(get_gateway())[AF_INET][0]['addr']
        else:
            ip_address = 'localhost'
            info("URL webapp: %s",  ', '.join(Msh.webapp_urls))
            info("URL oauth %s", ', '.join(Msh.oauth_urls))
        info("Server in ascolto su http://%s:%s", ip_address, porta)
        if XmlReader.settings["ambiente"] == 'PROD':
            httpserver.serve(Msh.app, host=ip_address, port=porta)  # pragma: no cover

    @staticmethod
    def check_server_connection(url, tentativi, riposo):
        server_on = False
        index = 0
        while index < tentativi and not server_on:
            cmd = "curl -I -m " + str(riposo) + " -X GET " + url
            response = execute_os_cmd(cmd)
            if response['return_code'] == 0 and response['cmd_out'].find("200 OK") > 0:
                server_on = True
                info("Server online")
            elif not response['return_code'] == 28:
                info("Attendo " + str(riposo) + " secondi...")
                sleep(riposo)
            index = index + 1
        return server_on

    @staticmethod
    def start_oauth():
        response = execute_os_cmd('pgrep node')
        if response['cmd_out'] == "":
            execute_os_cmd("sudo service oauth start")
        else:
            info("Oauth server is already running")

    @staticmethod
    def start_serveo():
        response = execute_os_cmd('pgrep autossh')
        if response['cmd_out'] == "":
            execute_os_cmd("sudo service serveo start")
        else:
            info("Serveo is already running")
        local = False
        oauth_url = "https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net"
        webapp_url = "https://" + XmlReader.settings['subdomain_webapp'] + ".serveo.net"
        if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net/login", 2, 5):
            execute_os_cmd("sudo service serveo restart")
            if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net/login", 2, 5):
                local = True
                oauth_url = ''
                webapp_url = ''
        return local, oauth_url, webapp_url

    @staticmethod
    def start_pagekite():
        response = execute_os_cmd('ps -aux | grep pagekite.py | grep python', check_out=True)
        if response['cmd_out'] == "":
            execute_os_cmd("sudo service pagekite start")
        else:
            info("Pagekite is already running")
        local = False
        oauth_url = "https://" + XmlReader.settings['subdomain_oauth_pagekite'] + ".pagekite.me"
        webapp_url = "https://" + XmlReader.settings['subdomain_webapp_pagekite'] + ".pagekite.me"
        if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth_pagekite'] + ".pagekite.me/login", 2, 5):
            execute_os_cmd("sudo service pagekite restart")
            if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth_pagekite'] + ".pagekite.me/login", 2, 5):
                local = True
                oauth_url = ''
                webapp_url = ''
        return local, oauth_url, webapp_url

    @staticmethod
    def start_dns_service(test_url, funzione, name):
        if Msh.check_server_connection(test_url, 2, 2):
            local, oauth_url, webapp_url = funzione()
            if not local:
                Msh.service_avaiable.append(name)
                Msh.oauth_urls.append(oauth_url)
                Msh.webapp_urls.append(webapp_url)


if __name__ == '__main__':
    Msh("settings.xml")  # pragma: no cover

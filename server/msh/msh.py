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
        (r'/static/(.*)', 'controller.Static'),
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
        Msh.start_service('ps -aux | grep node | grep server.js', 'oauth')
        if Msh.check_server_connection("http://www.google.com", 15, 5):
            Msh.start_dns_service("http://serveo.net", "serveo", 'ps -aux | grep serveo | grep 65177', '.serveo.net')
            Msh.start_dns_service("http://pagekite.net", "pagekite", 'ps -aux | grep pagekite.py | grep python', '.pagekite.me')
        if len(Msh.service_avaiable) == 0:
            info("Avvio solo in locale")
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
    def start_service(cmd_live, name):
        response = execute_os_cmd(cmd_live, check_out=True)
        if len(response['cmd_out'].split("\n")) <= 2:
            execute_os_cmd("sudo service " + name + " start")
        else:
            info("%s is already running", name)

    @staticmethod
    def final_check(name, dominio):
        local = False
        oauth_url = "https://" + XmlReader.settings['subdomain_oauth_' + name] + dominio
        webapp_url = "https://" + XmlReader.settings['subdomain_webapp_' + name] + dominio
        if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth_' + name] + dominio + "/login", 3, 5):
            execute_os_cmd("sudo service " + name + " restart")
            if not Msh.check_server_connection("https://" + XmlReader.settings['subdomain_oauth_' + name] + dominio + "/login", 3, 5):
                local = True
                oauth_url = ''
                webapp_url = ''
        return local, oauth_url, webapp_url

    @staticmethod
    def start_dns_service(test_url, name, cmd_live, dominio):
        if Msh.check_server_connection(test_url, 2, 2):
            Msh.start_service(cmd_live, name)
            local, oauth_url, webapp_url = Msh.final_check(name, dominio)
            if not local:
                Msh.service_avaiable.append(name)
                Msh.oauth_urls.append(oauth_url)
                Msh.webapp_urls.append(webapp_url)


if __name__ == '__main__':
    Msh("settings.xml")  # pragma: no cover

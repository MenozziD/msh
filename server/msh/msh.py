from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module import XmlReader, execute_os_cmd, check_server_connection
from controller import handle_error
from string import ascii_letters, digits
from random import choice
from netifaces import AF_INET, gateways, ifaddresses


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


def main(settings_path):
    XmlReader(settings_path)
    basicConfig(
        filename=XmlReader.settings['log']['filename'],
        format=XmlReader.settings['log']['format'],
        level=XmlReader.settings['log']['level'])
    porta = '65177'
    ip_address = 'localhost'
    response = execute_os_cmd('pgrep node')
    local = True
    if response['cmd_out'] == "":
        execute_os_cmd("sudo service oauth start")
    else:
        info("Oauth server is already running")
    if check_server_connection("http://www.google.com", 10, 5) and check_server_connection("http://serveo.net", 2, 5):
        response = execute_os_cmd('pgrep autossh')
        if response['cmd_out'] == "":
            execute_os_cmd("sudo service serveo start")
        else:
            info("Serveo is already running")
        local = False
        if not check_server_connection("https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net/login", 5, 5):
            execute_os_cmd("sudo service serveo restart")
            if not check_server_connection("https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net/login", 5, 5):
                local = True
    if local:
        info("Avvio solo in locale")
        execute_os_cmd("sudo service serveo stop")
        ip_address = ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['addr']
    else:
        info("URL webapp: %s", "https://" + XmlReader.settings['subdomain_webapp'] + ".serveo.net")
        info("URL oauth %s", "https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net")
    info("Server in ascolto su http://%s:%s", ip_address, porta)
    if XmlReader.settings["ambiente"] == 'PROD':
        httpserver.serve(app, host=ip_address, port=porta)  # pragma: no cover
    else:
        return True


if __name__ == '__main__':
    main("settings.xml")  # pragma: no cover

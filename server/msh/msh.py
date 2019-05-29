from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module import XmlReader
from controller import handle_error
from os import system


config = {
    'webapp3_extras.sessions': {
        'secret_key': 'uye569YTu4hTDdud7dghid6e7EDy'
    }
}

app = WSGIApplication([
    ('/api/net_cmd', 'controller.NetCmd'),
    ('/api/net_device', 'controller.NetDevice'),
    ('/api/net_scan', 'controller.NetScan'),
    ('/api/home', 'controller.Home'),
    ('/api/login', 'controller.Login'),
    ('/api/user', 'controller.User'),
    ('/logout', 'controller.Logout'),
    ('/favicon.ico', 'controller.Icon'),
    ('/', 'controller.Index'),
    (r'/static/(\D+)', 'controller.Static'),
], config=config, debug=True)
app.error_handlers[404] = handle_error
app.error_handlers[405] = handle_error
app.error_handlers[500] = handle_error


def main():
    XmlReader()
    basicConfig(
        filename=XmlReader.settings['log']['filename'],
        format=XmlReader.settings['log']['format'],
        level=XmlReader.settings['log']['level'])
    ip_address = 'localhost'
    port = '65177'
    system("ssh -o \"StrictHostKeyChecking no\" -R " + XmlReader.settings['subdomain_webapp'] + ":80:localhost:65177 -R " + XmlReader.settings['subdomain_oauth'] + ":80:localhost:3000 serveo.net 1> /dev/null 2> /dev/null &")
    info("URL webapp: %s", "https://" + XmlReader.settings['subdomain_webapp'] + ".serveo.net")
    info("URL oauth %s", "https://" + XmlReader.settings['subdomain_oauth']  + ".serveo.net")
    info("Server in ascolto su http://%s:%s", ip_address, port)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

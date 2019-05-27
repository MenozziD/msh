from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module.xml_reader import XmlReader
from controller.net_cmd import NetCmd
from controller.net_scan import NetScan
from controller.net_device import NetDevice
from controller.home import Home
from controller.static import Icon, Index, Static, handle_error
from urllib import request
from json import loads
from os import system


app = WSGIApplication([
    ('/api/net_cmd', NetCmd),
    ('/api/net_device', NetDevice),
    ('/api/net_scan', NetScan),
    ('/api/home', Home),
    ('/api/login', Login),
    ('/favicon.ico', Icon),
    ('/', Index),
    (r'/static/(\D+)', Static),
], debug=True)
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
    f = open("action.json", "r")
    cont = f.read()
    f.close()
    f1 = open("settings.xml", "r")
    sett = f1.read()
    f1.close()
    old_hostname = cont.split("\"url\": \"")[1].split("\"")[0].split("/api/home")[0]
    old_hostname_auth_token = cont.split("\"authenticationUrl\": \"")[1].split("\"")[0].split("/oauth")[0]
    response = loads(request.urlopen("http://127.0.0.1:4040/api/tunnels").read().decode('utf-8'))
    new_hostname = ''
    new_hostname_auth_token = ''
    for tunnel in response['tunnels']:
        if tunnel['public_url'].find('https') == 0 and tunnel['config']['addr'].find(port) > 0:
            new_hostname = tunnel['public_url']
        if tunnel['public_url'].find('https') == 0 and tunnel['config']['addr'].find('3000') > 0:
            new_hostname_auth_token = tunnel['public_url']
    if new_hostname != old_hostname:
        cont = cont.replace(old_hostname, new_hostname)
        cont = cont.replace(old_hostname_auth_token, new_hostname_auth_token)
        sett = sett.replace(old_hostname, new_hostname)
        f = open("action.json", "w")
        f.write(cont)
        f.close()
        f = open("settings.xml", "w")
        f.write(sett)
        f.close()
        system("gactions update --action_package action.json --project " + XmlReader.settings['project_id_google_actions'])
        info("URL oauth: %s", new_hostname_auth_token + "/oauth")
        info("URL token: %s", new_hostname_auth_token + "/token")
    XmlReader()
    info("Server in ascolto su http://%s:%s", ip_address, port)
    info("URL webapp: %s", new_hostname)
    info("URL fake server %s", new_hostname_auth_token)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

from webapp3 import WSGIApplication
from logging import basicConfig, info, exception
from paste import httpserver
from module import XmlReader
from controller import handle_error
from subprocess import run, PIPE
from os import system
from string import ascii_letters, digits
from random import choice
from time import sleep


def main():
    try:
        XmlReader()
        basicConfig(
            filename=XmlReader.settings['log']['filename'],
            format=XmlReader.settings['log']['format'],
            level=XmlReader.settings['log']['level'])
        ip_address = 'localhost'
        port = '65177'
        cmd = 'pgrep node'
        info("Eseguo comando: %s", cmd)
        cmd = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1]
        if cmd_out == "":
            cmd = "sudo service oauth start"
            info("Eseguo comando: %s", cmd)
            system(cmd)
        else:
            info("Oauth server is already running")
        cmd = 'pgrep autossh'
        info("Eseguo comando: %s", cmd)
        cmd = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1]
        if cmd_out == "":
            internet = False
            while not internet:
                cmd = "curl -I -X GET http://www.google.com"
                info("Eseguo comando: %s", cmd)
                cmd = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
                if cmd.returncode == 0 and str(cmd.stdout)[2:-1].find("200 OK") > 0:
                    internet = True
                    info("Connessione internet presente")
                    cmd = "sudo service serveo start"
                    info("Eseguo comando: %s", cmd)
                    system(cmd)
                else:
                    info("Attendo 10 secondi...")
                    sleep(10)
        else:
            info("Serveo is already running")
        info("URL webapp: %s", "https://" + XmlReader.settings['subdomain_webapp'] + ".serveo.net")
        info("URL oauth %s", "https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net")
        info("Server in ascolto su http://%s:%s", ip_address, port)
        config = {
            'webapp3_extras.sessions': {
                'secret_key': ''.join(choice(ascii_letters + digits) for i in range(36))
            }
        }
        app = WSGIApplication([
            ('/api/net_cmd', 'controller.NetCmd'),
            ('/api/net_device', 'controller.NetDevice'),
            ('/api/net_scan', 'controller.NetScan'),
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
        httpserver.serve(app, host=ip_address, port=port)
    except Exception:
        exception("Exception")


if __name__ == '__main__':
    main()

from webapp3 import WSGIApplication
from logging import basicConfig, info, exception
from paste import httpserver
from module import XmlReader, execute_os_cmd
from controller import handle_error
from string import ascii_letters, digits
from random import choice
from time import sleep


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


def main():
    try:
        XmlReader("settings.xml")
        basicConfig(
            filename=XmlReader.settings['log']['filename'],
            format=XmlReader.settings['log']['format'],
            level=XmlReader.settings['log']['level'])
        ip_address = 'localhost'
        port = '65177'
        cmd = 'pgrep node'
        response = execute_os_cmd(cmd)
        if response['cmd_out'] == "":
            cmd = "sudo service oauth start"
            execute_os_cmd(cmd)
        else:
            info("Oauth server is already running")
        cmd = 'pgrep autossh'
        response = execute_os_cmd(cmd)
        if response['cmd_out'] == "":
            internet = False
            while not internet:
                cmd = "curl -I -X GET http://www.google.com"
                response = execute_os_cmd(cmd)
                if response['return_code'] == 0 and response['cmd_out'].find("200 OK") > 0:
                    internet = True
                    info("Connessione internet presente")
                    cmd = "sudo service serveo start"
                    execute_os_cmd(cmd)
                else:
                    info("Attendo 10 secondi...")
                    sleep(10)
        else:
            info("Serveo is already running")
        info("URL webapp: %s", "https://" + XmlReader.settings['subdomain_webapp'] + ".serveo.net")
        info("URL oauth %s", "https://" + XmlReader.settings['subdomain_oauth'] + ".serveo.net")
        info("Server in ascolto su http://%s:%s", ip_address, port)
        httpserver.serve(app, host=ip_address, port=port)
    except Exception:
        exception("Exception")


if __name__ == '__main__':
    main()

from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module import XmlReader
from controller import handle_error
from subprocess import run, PIPE
from crontab import CronTab
from ngrok import update_url

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
    cmd = run(['pwd'], stdout=PIPE, stderr=PIPE)
    cmd_out = str(cmd.stdout)[2:-1].replace("\\n", "")
    new_url = update_url('msh')
    my_cron = CronTab(user=True)
    job = my_cron.new(command='cd ' + cmd_out + ' && python3 ' + cmd_out + '/ngrok.py')
    job.hour.every(7)
    my_cron.write()
    info("Server in ascolto su http://%s:%s", ip_address, port)
    info("URL webapp: %s", new_url['webapp'])
    info("URL fake server %s", new_url['auth'])
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

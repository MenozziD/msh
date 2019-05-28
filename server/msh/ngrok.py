from urllib import request
from json import loads
from os import system
from module import XmlReader
from logging import basicConfig, info
from time import sleep


def update_url(invocator):
    if invocator == 'cron':
        XmlReader()
        basicConfig(
            filename='cron.log',
            format=XmlReader.settings['log']['format'],
            level=XmlReader.settings['log']['level'])
        info("Eseguo kill porcesso ngrok")
        system("ps -aux | grep ngrok | grep yaml | awk '{print $2}' | xargs kill -9")
        info("Restrat ngrok")
        system("ngrok start --config=../ngrok/ngrok.yaml --all 1> /dev/null 2> /dev/null &")
        sleep(5)
    url = {}
    f = open('action.json', "r")
    cont = f.read()
    f.close()
    old_hostname = cont.split("\"url\": \"")[1].split("\"")[0].split("/api/home")[0]
    old_hostname_auth_token = cont.split("\"authenticationUrl\": \"")[1].split("\"")[0].split("/oauth")[0]
    response = loads(request.urlopen("http://127.0.0.1:4040/api/tunnels").read().decode('utf-8'))
    new_hostname = ''
    new_hostname_auth_token = ''
    for tunnel in response['tunnels']:
        if tunnel['public_url'].find('https') == 0 and tunnel['config']['addr'].find('65177') > 0:
            new_hostname = tunnel['public_url']
        if tunnel['public_url'].find('https') == 0 and tunnel['config']['addr'].find('3000') > 0:
            new_hostname_auth_token = tunnel['public_url']
    if new_hostname != old_hostname:
        cont = cont.replace(old_hostname, new_hostname)
        cont = cont.replace(old_hostname_auth_token, new_hostname_auth_token)
        f = open('action.json', "w")
        f.write(cont)
        f.close()
        # system("gactions update --action_package action.json --project " + XmlReader.settings['project_id_google_actions'])
        info("URL webapp: %s", new_hostname)
        info("URL fake server %s", new_hostname_auth_token)
    url['webapp'] = new_hostname
    url['auth'] = new_hostname_auth_token
    return url


if __name__ == '__main__':
    update_url('cron')

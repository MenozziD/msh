from logging import info, exception
from pexpect import pxssh
from module import XmlReader, DbManager
from subprocess import run, PIPE, check_output
from datetime import datetime
from json import dumps, load
from os import system
from urllib import request
from time import sleep


def execute_os_cmd(cmd, check_out=False, sys=False):
    response = {}
    if XmlReader.settings["ambiente"] == 'PROD':
        info("Eseguo comando: %s", cmd)
        if not check_out and not sys:
            cmd = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
            cmd_out = str(cmd.stdout)[2:-1].replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
            cmd_err = str(cmd.stderr)[2:-1].replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
            info("Return Code: %s", cmd.returncode)
            info("Output: %s", cmd_out)
            info("Error: %s", cmd_err)
            response = {
                'return_code': cmd.returncode,
                'cmd_out': cmd_out,
                'cmd_err': cmd_err
            }
        else:
            if check_out:
                cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
                info("Output: %s", cmd_out)
                response = {'cmd_out': cmd_out}
            else:
                system(cmd)
    else:
        f = open('command_simulate.json', 'r')
        response = load(f)
        f.close()
    return response


def execute_ssh_cmd(ip, usr, psw, cmd):
    if XmlReader.settings["ambiente"] == 'PROD':
        login = False
        ss = None
        response = {}
        try:
            ss = pxssh.pxssh()
            ss.login(ip, usr, psw)
            login = True
            info("Eseguo comando in SSH: %s", cmd)
            ss.sendline(cmd)
            ss.prompt()
            response['cmd_out'] = str(ss.before)[2:-1].replace("\\r\\n", '\r\n')
            info("Output: %s", response['cmd_out'])
            response['output'] = 'OK'
        except Exception as e:
            exception("Exception")
            if str(e) == "password refused":
                response['output'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 13)
            else:
                response['output'] = str(e)
        finally:
            if login:
                ss.logout()
    else:
        f = open('command_simulate.json', 'r')
        response = load(f)
        f.close()
    return response


def execute_request_http(url):
    if XmlReader.settings["ambiente"] == 'PROD':
        info("MAKE REQUEST: %s", url)
        response = request.urlopen(url).read().decode('utf-8')
        info("RESPONSE: %s", response)
    else:
        f = open('request_simulate.json', 'r')
        response = f.read()
        if response == "\"b'MAC info'\"":
            response = "b'MAC info'"
        f.close()
    return response


def check_internet_connection():
    internet = False
    while not internet:
        cmd = "curl -I -X GET http://www.google.com"
        response = execute_os_cmd(cmd)
        if response['return_code'] == 0 and response['cmd_out'].find("200 OK") > 0:
            internet = True
            info("Connessione internet presente")
        else:
            info("Attendo 10 secondi...")
            sleep(10)
            if XmlReader.settings["ambiente"] == "TEST":
                internet = True
    return internet


def set_api_response(response_payload, response, timmestamp=True):
    DbManager.close_db()
    if timmestamp:
        response_payload['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    response.write(dumps(response_payload, indent=4, sort_keys=True))
    info("RESPONSE CODE: %s", response.status)
    info("RESPONSE PAYLOAD: %s", response_payload)


def validate_format(request_validate):
    try:
        request_validate.json
    except ValueError:
        return False
    return True

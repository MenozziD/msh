from logging import info, exception
from pexpect import pxssh
from module import XmlReader, DbManager
from subprocess import run, PIPE, check_output
from datetime import datetime
from json import dumps, load
from os import system
from urllib import request
from netifaces import gateways


def execute_os_cmd(cmd, check_out=False, sys=False):
    response = {}
    if XmlReader.settings["ambiente"] == 'PROD':
        try:
            info("Eseguo comando: %s", cmd)
            if not check_out and not sys:
                response = execute_os_cmd_with_run(cmd)
            else:
                if check_out:
                    cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
                    info("Output: %s", cmd_out)
                    response = {'cmd_out': cmd_out}
                else:
                    system(cmd)
        except Exception as e:
            exception(e)
            response = {
                'return_code': -1,
                'cmd_out': '',
                'cmd_err': str(e)
            }
    else:
        f = open('command_simulate.json', 'r')
        response = load(f)
        f.close()
    return response


def execute_os_cmd_with_run(cmd):
    cmd_exec = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    cmd_out = str(cmd_exec.stdout)[2:-1].replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
    cmd_err = str(cmd_exec.stderr)[2:-1].replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
    info("Return Code: %s", cmd_exec.returncode)
    info("Output: %s", cmd_out)
    info("Error: %s", cmd_err)
    if cmd_err == "" and cmd_exec.returncode != 0 and cmd.find("ping") == -1:
        cmd_err = cmd_out
    response = {
        'return_code': cmd_exec.returncode,
        'cmd_out': cmd_out,
        'cmd_err': cmd_err
    }
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
                response['output'] = get_string(13)
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
        try:
            response = request.urlopen(url).read().decode('utf-8')
        except Exception as e:
            exception("Exception")
            response = "Error " + str(e)
        info("RESPONSE: %s", response)
    else:
        f = open('request_simulate.json', 'r')
        response = f.read()
        if response == "\"b'MAC info'\"":
            response = "b'MAC info'"
        f.close()
    return response


def get_gateway():
    gateway = ''
    for path, node in traverse(gateways()):
        if isinstance(node, tuple) and node[0].find('192.168') == 0 and ('default' in path or gateway == ''):
                gateway = node[1]
    return gateway


def set_api_response(response_payload, response, timmestamp=True, close_db=True):
    if close_db:
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


def evaluate(command, data=None, dev=None, result=None, parametri=None):
    from module import cmd_ping, cmd_pcwin, cmd_radio, cmd_esp
    info("ESEGUO CON EVALUATE: %s", command)
    return eval(command)


def get_string(indice, da_sostiuire=None, da_aggiungere=None):
    to_return = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], indice)
    if da_sostiuire is not None:
        to_return = to_return.replace("%s", da_sostiuire)
    if da_aggiungere is not None:
        to_return = to_return + da_aggiungere
    return to_return


def traverse(dict_or_list, path=None):
    if path is None:
        path = []
    if isinstance(dict_or_list, dict):
        iterator = dict_or_list.items()
    else:
        iterator = enumerate(dict_or_list)
    for k, v in iterator:
        yield path + [k], v
        if isinstance(v, (dict, list)):
            for k1, v1 in traverse(v, path + [k]):
                yield k1, v1

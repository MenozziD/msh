from logging import info
from module import XmlReader
from subprocess import run, PIPE, check_output
from datetime import datetime
from json import dumps, load
from os import system


def execute_os_cmd(cmd, check_out=False, sys=False):
    response = {}
    if XmlReader.settings["ambiente"] == 'PROD':
        info("Eseguo comando: %s", cmd)
        if not check_out and not sys:
            cmd = run(cmd.split(" "), stdout=PIPE, stderr=PIPE)
            cmd_out = str(cmd.stdout)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
            cmd_err = str(cmd.stderr)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
            response = {
                'return_code': cmd.returncode,
                'cmd_out': cmd_out,
                'cmd_err': cmd_err
            }
        else:
            if check_out:
                cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                response = {'cmd_out': cmd_out}
            else:
                system(cmd)
    else:
        f = open('command_simulate.json', 'r')
        response = load(f)
        f.close()
    return response


def set_api_response(response_payload, response):
    response_payload['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    response.write(dumps(response_payload, indent=4, sort_keys=True))
    info("RESPONSE CODE: %s", response.status)
    info("RESPONSE PAYLOAD: %s", response_payload)


def validate_format(request):
    try:
        request.json
    except ValueError:
        return False
    return True

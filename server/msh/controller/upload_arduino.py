from controller import BaseHandler
from logging import info, exception
from json import dumps, loads
from module import XmlReader
from datetime import datetime
from subprocess import PIPE, run, check_output
from urllib import request


class UploadArduino(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            if self.session.get('user') is not None and self.session.get('role') == 'ADMIN':
                data = loads(body)
                tipo_operazione = data['tipo_operazione']
                core = data['core']
                tipologia = data['tipologia']
                if tipo_operazione == "upload":
                    cmd = "arduino-cli board list | grep tty | awk '{print $1}'"
                    usb = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "").replace("\\t", "")
                    if usb != "":
                        run(["mkdir", tipologia])
                        run(["curl", "https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/" + tipologia + "/" + tipologia + ".ino", "--output", tipologia + "/" + tipologia + ".ino"])
                        run(["curl", "https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/" + tipologia + "/index.h", "--output", tipologia + "/" + "index.h"])
                        cmd = "arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'"
                        fqbn = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "").replace("\\t", "")
                        info("fqbn: %s usb: %s", fqbn, usb)
                        compile = run(["sudo", "arduino-cli", "compile", "--fqbn", fqbn, tipologia], stdout=PIPE, stderr=PIPE)
                        cmd_out_split = str(compile.stdout)[2:-1].replace("\\n", "\n").split('\n')
                        program_info = cmd_out_split[1]
                        memory_info = cmd_out_split[2]
                        compile_output = {
                            'program_bytes_used': program_info.split("uses ")[1].split(" bytes")[0],
                            'program_percentual_used': program_info.split("(")[1].split(")")[0],
                            'program_bytes_total': program_info.split("Maximum is ")[1].split(" bytes")[0],
                            'memory_bytes_used': memory_info.split("use ")[1].split(" bytes")[0],
                            'memory_percentual_used': memory_info.split("(")[1].split(")")[0],
                            'memory_bytes_free': memory_info.split("leaving ")[1].split(" bytes")[0],
                            'memory_bytes_total': memory_info.split("Maximum is ")[1].split(" bytes")[0]
                        }
                        response['compile_output'] = compile_output
                        upload = run(["sudo", "arduino-cli", "upload", "-p", usb, "--fqbn", fqbn, tipologia], stdout=PIPE, stderr=PIPE)
                        upload_err = str(upload.stderr)[2:-1].replace("\\n", "\n")
                        run(["sudo", "rm", "-rf", tipologia])
                        if upload_err == "":
                            cmd_out = str(upload.stdout)[2:-1].replace("\\n", "\n").replace("\\r", "")
                            upload_output = {
                                'porta_seriale': cmd_out.split("Serial port ")[1].split("\n")[0],
                                'chip': cmd_out.split("Chip is ")[1].split("\n")[0],
                                'mac_addres': cmd_out.split("MAC: ")[1].split("\n")[0],
                                'byte_write': cmd_out.split("Wrote ")[1].split(" bytes")[0],
                                'byte_write_compressed': cmd_out.split("Wrote ")[1].split(" compressed)")[0].split("(")[0],
                                'time': cmd_out.split(" (effective")[0].split("compressed) at ")[1].split(" in ")[1]
                            }
                            response['upload_output'] = upload_output
                            response['output'] = 'OK'
                        else:
                            response['output'] = upload_err
                    else:
                        response['output'] = 'Nessun dispositivo collegato'
                if tipo_operazione == "core":
                    cmd = "arduino-cli board listall | awk '{$NF=\"\"; print $0}'"
                    cmd_out = str(check_output(cmd, shell=True))[2:-1].replace("\\n", "\n").replace("\\t", "\t")
                    cores = []
                    for core in cmd_out.split("\n")[1:]:
                        if core != '':
                            cores.append(core[:-1])
                    response['cores'] = cores
                    response['output'] = 'OK'
                if tipo_operazione == "tipo":
                    url = "https://api.github.com/repos/VanMenoz92/msh/contents/devices?ref=master"
                    res = loads(request.urlopen(url).read().decode('utf-8'))
                    types = []
                    for device in res:
                        types.append(device['name'])
                    response['types'] = types
                    response['output'] = 'OK'
            else:
                response['output'] = 'Devi effettuare la login per utilizzare questa API'
                if self.session.get('role') == 'USER':
                    response['output'] = 'La funzione richiesta può essere eseguita solo da un ADMIN'
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            info("RESPONSE CODE: %s", self.response.status)
            info("RESPONSE PAYLOAD: %s", response)

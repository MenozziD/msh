from controller import BaseHandler
from logging import info, exception
from module import set_api_response, validate_format
from module import DbManager
from json import loads, dumps


def prova(uno, due, tre):
    info("%s %s %s", uno, due, tre)
    if due == "online":
        to_return = "ON"
    else:
        to_return = "OFF"
    return to_return


class Home(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            DbManager()
            response = Home.check(self.request, body)
            if response['output'] == 'OK':
                data = self.request.json
                intent = data['inputs'][0]['intent']
                funzioni = {
                    "action.devices.SYNC": Home.sync,
                    "action.devices.QUERY": Home.query,
                    "action.devices.EXECUTE": Home.execute
                }
                response = funzioni[intent](data)
            else:
                raise Exception(response['output'])
        except Exception:
            exception("Exception")
        finally:
            set_api_response(response, self.response, False)

    @staticmethod
    def check(request, body):
        response = {}
        if body != "" and validate_format(request):
            response['output'] = 'OK'
        else:
            if body != "":
                response['output'] = "Il payload deve essere in formato JSON"
            else:
                response['output'] = "Questa API ha bisogno di un payload"
        return response

    @staticmethod
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
                for k1, v1 in Home.traverse(v, path + [k]):
                    yield k1, v1

    @staticmethod
    def iter_json(json_data, path, index, size):
        if index < size:
            json_data[path[index]] = Home.iter_json(json_data[path[index]], path, index + 1, size)
            return json_data
        else:
            return True if json_data == "ON" else False

    @staticmethod
    def create_response(template, dev, data=None):
        funzione = ""
        for path, node in Home.traverse(template):
            if str(node)[0:1] != "{" and str(node)[0:1] != "[":
                for i in path:
                    if str(i).find("[") > 0:
                        # CHIAVE DA LEGGERE
                        template = loads(dumps(template, indent=4, sort_keys=True).replace(i, eval(i)))
        for path, node in Home.traverse(template):
            if str(node)[0:1] != "{" and str(node)[0:1] != "[":
                if str(node).find("[") > 0 and str(node).find("(") == -1:
                    # VALORE DA LEGGERE
                    template = loads(dumps(template, indent=4, sort_keys=True).replace(node, eval(node)))
                else:
                    if str(node).find("(") > 0:
                        # FUNZIONE DA INVOCARE
                        funzione = node
                        if node.find("[") > 0:
                            # FUNZIONE CON PARAMETRI NON STATICI
                            parametri = node.split("(")[1].split(")")[0]
                            if parametri.find(", ") > 0:
                                for parametro in parametri.split(", "):
                                    if parametro.find("[") > 0:
                                        funzione = funzione.replace(parametro, "'" + eval(parametro) + "'")
                            else:
                                if parametri.find("[") > 0:
                                    funzione = funzione.replace(parametri, "'" + eval(parametri) + "'")
                        value = eval(funzione)
                        template = loads(dumps(template, indent=4, sort_keys=True).replace(node, value))
                        if value in ("ON", "OFF"):
                            template = Home.iter_json(template, path, 0, len(path))
        return template

    @staticmethod
    def read_request(template):
        for path, node in Home.traverse(template):
            if len(path) >= 2 and str(node)[0:1] != "{":
                info("PARAMETRO: %s TIPOLOGIA: %s", path[-1], node)

    @staticmethod
    def sync(data):
        devices = []
        device_type = DbManager.select_tb_net_device_and_google_info()
        for dev in device_type:
            devices.append(Home.create_response(dev['sync_response'], dev))
        response = {
            'requestId': data['requestId'],
            'payload': {
                "agentUserId": "01011980",
                'devices': devices}
        }
        return response

    @staticmethod
    def query(data):
        device = DbManager.select_tb_net_device_and_google_info(net_mac=data["inputs"][0]["payload"]["devices"][0]["id"])[0]
        return Home.create_response(device['query_response'], device, data)

    @staticmethod
    def execute(data):
        '''
        req_command = data['inputs'][0]['payload']['commands'][0]
        command = req_command['execution'][0]['command']
        params = req_command['execution'][0]['params']
        device_id = req_command['devices'][0]['id']
        if command == 'action.devices.commands.OnOff':
            if device_id == 'A0:4F:D4:B4:3A:53':
                info('device A0:4F:D4:B4:3A:53 %s', params['on'])
                # cmd_esp('192.168.1.9', 'toggle')
            if device_id == '2':
                info('ON/OFF device 2')
        if command == 'action.devices.commands.ColorAbsolute' and device_id == '2':
                info('colore device 2 %s', params['color']['spectrumRGB'])
        '''
        device = DbManager.select_tb_net_device_and_google_info(
            net_mac=data["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"])[0]
        data1 = {
            "command": "action.devices.commands.OnOff",
            "params": {
                "color": {
                    "name": "magenta",
                    "spectrumRGB": 16711935
                },
                "color1": {
                    "spectrumHSV": {
                        "hue": 240.0,
                        "saturation": 1.0,
                        "value": 1.0
                    }
                },
                "on": True
            }
        }
        Home.read_request(data1)
        return Home.create_response(device['execute_response_ok'], device, data)

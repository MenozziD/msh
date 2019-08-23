from controller import BaseHandler
from logging import info, exception
from module import set_api_response, validate_format, DbManager, prova
from json import loads, dumps


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
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
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
    def iter_json(json_data, path, index, size, primo, secondo, terzo):
        if index < size:
            json_data[path[index]] = Home.iter_json(json_data[path[index]], path, index + 1, size, primo, secondo, terzo)
            return json_data
        else:
            return primo if json_data == secondo else terzo

    @staticmethod
    def create_response(template, dev, data=None, result=None):
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
                            template = Home.iter_json(template, path, 0, len(path), True, "ON", False)
        return template

    @staticmethod
    def read_request(template):
        for path, node in Home.traverse(template):
            if str(node)[0:1] != "{":
                if type(node).__name__ == 'bool':
                    template = Home.iter_json(template, path, 0, len(path), "ON", True, "OFF")
        return template

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
        """
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
        "on": true
        """
        dev = DbManager.select_tb_net_device_and_google_info(net_mac=data["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"])[0]
        parametri = Home.read_request(data["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"])
        result = {}
        for key in parametri.keys():
            result = eval(dev['execute_request'][key])
        if result['output'] == 'OK':
            response = Home.create_response(dev['execute_response_ok'], dev, data)
        else:
            response = Home.create_response(dev['execute_response_ko'], dev, data, result=result)
        return response

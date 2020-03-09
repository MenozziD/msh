from controller import BaseHandler
from logging import info, exception
from module import set_api_response, validate_format, DbManager, evaluate, verify_token, get_string, traverse
from json import loads, dumps


class Home(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            response = Home.check(self.request, body, self.request.headers)
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
            set_api_response(response, self.response, timmestamp=False)

    @staticmethod
    def check(request, body, headers_list):
        response = {}
        if body != "" and validate_format(request):
            if 'Authorization' in headers_list and headers_list['Authorization'].find("Bearer ") == 0 and verify_token(headers_list['Authorization'].replace("Bearer ", ""))['output'] == 'OK':
                response['output'] = 'OK'
            else:
                response = Home.check_header(headers_list)
        else:
            if body != "":
                response['output'] = response['output'] = get_string(22)
            else:
                response['output'] = response['output'] = get_string(21)
        return response

    @staticmethod
    def check_header(headers_list):
        response = {}
        if 'Authorization' in headers_list:
            if headers_list['Authorization'].find("Bearer ") == 0:
                response['output'] = get_string(41)
            else:
                response['output'] = get_string(40, da_sostiuire="Authorization", da_aggiungere="Bearer Token")
        else:
            response['output'] = get_string(39, da_aggiungere="Authorization")
        return response

    @staticmethod
    def create_response(template, dev, data=None, result=None):
        template = Home.read_key(template, data)
        for path, node in traverse(template):
            if isinstance(node, str) and (str(node).find("(") > 0 or str(node).find("[") > 0):
                value = evaluate(node, data, dev, result)
                if not isinstance(value, str):
                    template = loads(dumps(template, indent=4, sort_keys=True).replace("\"" + node + "\"", str(value)))
                else:
                    template = loads(dumps(template, indent=4, sort_keys=True).replace(node, value))
        template = loads(dumps(template, indent=4, sort_keys=True).replace("\"ON\"", "true").replace("\"OFF\"", "false"))
        template = loads(dumps(template, indent=4, sort_keys=True).replace("\"ON\"", "true").replace("\"OFF\"", "false"))
        return template

    @staticmethod
    def read_key(template, data):
        chiavi_da_sostituire = []
        for path, node in traverse(template):
            for i in path:
                if str(i).find("[") > 0 and str(i) not in chiavi_da_sostituire:
                    chiavi_da_sostituire.append(i)
        for key in chiavi_da_sostituire:
            template = loads(dumps(template, indent=4, sort_keys=True).replace(key, evaluate(key, data)))
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
        google_params = data["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]
        google_params = loads(dumps(google_params, indent=4, sort_keys=True).replace("true", "\"ON\"").replace("false", "\"OFF\""))
        result = {}
        for key in google_params.keys():
            result = evaluate(dev['execute_request'][key], dev=dev, parametri=google_params)
        if result['output'] == 'OK':
            response = Home.create_response(dev['execute_response_ok'], dev, data)
        else:
            response = Home.create_response(dev['execute_response_ko'], dev, data, result)
        return response

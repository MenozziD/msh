from controller import BaseHandler
from logging import info, exception
from module import set_api_response, validate_format
from module import cmd_esp


class Home(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
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
                response['output'] = 'OK'
            else:
                raise Exception(response['output'])
        except Exception as e:
            exception("Exception")
            response['output'] = str(e)
        finally:
            set_api_response(response, self.response)

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
    def sync(data):
        devices = []
        device = {
            'id': '1',
            'type': 'action.devices.types.SWITCH',
            'traits': ['action.devices.traits.OnOff'],
            'name': {'name': 'fan'},
            'willReportState': True
        }
        devices.append(device)
        device = {
            'id': '2',
            'type': 'action.devices.types.LIGHT',
            'traits': ['action.devices.traits.OnOff', 'action.devices.traits.ColorSpectrum'],
            'name': {'name': 'lights'},
            'willReportState': True
        }
        devices.append(device)
        device = {
            'id': '3',
            "type": "action.devices.types.THERMOSTAT",
            'traits': ['action.devices.traits.TemperatureSetting'],
            'name': {
                'name': 'temperature'
            },
            'willReportState': True,
            "attributes": {
                "thermostatTemperatureUnit": "C"
            },
        }
        devices.append(device)
        response = {
            'requestId': data['requestId'],
            'payload': {'devices': devices}
        }
        return response

    @staticmethod
    def query(data):
        first = {
            'on': True,
            'online': True
        }
        second = {
            'on': False,
            'online': True,
            'color': {
                'spectrumRGB': 16510692
            }
        }
        third = {
            "online": True,
            "thermostatTemperatureAmbient": 25.1,
            "thermostatHumidityAmbient": 45.3
        }
        devices = {
            '1': first,
            '2': second,
            '3': third
        }
        response = {
            'requestId': data['requestId'],
            'payload': {'devices': devices}
        }
        return response

    @staticmethod
    def execute(data):
        response = {}
        req_command = data['inputs'][0]['payload']['commands'][0]
        command = req_command['execution'][0]['command']
        params = req_command['execution'][0]['params']
        device_id = req_command['devices'][0]['id']
        if command == 'action.devices.commands.OnOff':
            if device_id == '1':
                info('device 1 %s', params['on'])
                # cmd_esp('192.168.1.9', 'toggle')
            if device_id == '2':
                info('ON/OFF device 2')
        if command == 'action.devices.commands.ColorAbsolute' and device_id == '2':
                info('colore device 2 %s', params['color']['spectrumRGB'])
        return response

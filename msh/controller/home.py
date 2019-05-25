from webapp3 import RequestHandler
from logging import info
from json import dumps, loads


class Home(RequestHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        data = loads(body)
        intent = data['inputs'][0]['intent']
        funzioni = {
            "action.devices.SYNC": Home.sync,
            "action.devices.QUERY": Home.query,
            "action.devices.EXECUTE": Home.execute
        }
        response = funzioni[intent](data)
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(dumps(response, indent=4, sort_keys=True))
        info("RESPONSE CODE: %s", self.response.status)
        info("RESPONSE PAYLOAD: %s", response)

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
        devices = {
            '1': first,
            '2': second
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
            if device_id == '2':
                info('ON/OFF device 2')
        if command == 'action.devices.commands.ColorAbsolute':
            if device_id == '2':
                info('colore device 2 %s', params['color']['spectrumRGB'])
        return response

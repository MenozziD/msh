from controller import BaseHandler
from logging import info, exception
from module import set_api_response, validate_format
from module import DbManager


class Home(BaseHandler):
    def post(self):
        body = str(self.request.body)[2:-1]
        info("%s %s", self.request.method, self.request.url)
        info("BODY %s", body)
        response = {}
        try:
            DbManager()
            if Home.check(self.request, body)['output'] == 'OK':
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
            DbManager.close_db()
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
    def sync(data):
        devices = []
        device_type = DbManager.select_tb_net_device_and_google_info()
        for dev in device_type:
            device = {
                'id': dev["net_mac"],
                'type': dev["google_type"],
                'traits': [dev["google_traits"].split(",")[:-1]],
                'name': {'name': dev["net_code"]},
                'willReportState': True
            }
            devices.append(device)
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
        google_device = {'on': device['net_status']}
        if device['net_online'] == 'OFF':
            google_device['online'] = False
        else:
            google_device['online'] = True
        devices = {
            data["inputs"][0]["payload"]["devices"][0]["id"]: google_device,
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
            if device_id == 'A0:4F:D4:B4:3A:53':
                info('device A0:4F:D4:B4:3A:53 %s', params['on'])
                # cmd_esp('192.168.1.9', 'toggle')
            if device_id == '2':
                info('ON/OFF device 2')
        if command == 'action.devices.commands.ColorAbsolute' and device_id == '2':
                info('colore device 2 %s', params['color']['spectrumRGB'])
        return response

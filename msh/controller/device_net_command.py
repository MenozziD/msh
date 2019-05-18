from webapp3 import RequestHandler
from logging import info, exception
from module.dbmanager import DbManager
from module.xml_reader import XmlReader
from json import dumps
from datetime import datetime


class DeviceNetCommand(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        response = {}
        try:
            dispositivo = self.request.get('d')
            DbManager(XmlReader.settings['path']['db'])
            rows = DbManager.select(XmlReader.settings['query']['select_net_command_for_type'] % dispositivo)
            commands = []
            for r in rows:
                commands.append(str(r[0]))
            DbManager.close_db()
            response['output'] = 'OK'
            response['commands'] = commands
        except Exception as e:
            exception("Exception")
            response['output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['net'], e)
        finally:
            response['timestamp'] = datetime.now().strftime(XmlReader.settings['timestamp'])
            self.response.headers.add('Access-Control-Allow-Origin', '*')
            self.response.headers.add('Content-Type', 'application/json')
            self.response.write(dumps(response, indent=4, sort_keys=True))
            info("RESPONSE CODE: %s", self.response.status)
            info("RESPONSE PAYLOAD: %s", response)

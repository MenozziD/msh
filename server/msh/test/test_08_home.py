from msh import app
from unittest import TestCase
from webapp3 import Request
from test import read_xml


class TestHome(TestCase):

    def test_no_payload(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_payload_sync(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.SYNC"' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_query(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.QUERY"' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_execute_on_off_device_1(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.EXECUTE",' \
                       b'           "payload": {' \
                       b'               "commands": [' \
                       b'                   {' \
                       b'                       "execution": [' \
                       b'                           {' \
                       b'                               "command":"action.devices.commands.OnOff",' \
                       b'                               "params": {' \
                       b'                                   "on": true' \
                       b'                               }' \
                       b'                           }' \
                       b'                       ],' \
                       b'                       "devices": [' \
                       b'                           {' \
                       b'                               "id":"1"' \
                       b'                           }' \
                       b'                       ]' \
                       b'                   }' \
                       b'               ]' \
                       b'            }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_execute_on_off_device_2(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.EXECUTE",' \
                       b'           "payload": {' \
                       b'               "commands": [' \
                       b'                   {' \
                       b'                       "execution": [' \
                       b'                           {' \
                       b'                               "command":"action.devices.commands.OnOff",' \
                       b'                               "params": {' \
                       b'                                   "on": true' \
                       b'                               }' \
                       b'                           }' \
                       b'                       ],' \
                       b'                       "devices": [' \
                       b'                           {' \
                       b'                               "id":"2"' \
                       b'                           }' \
                       b'                       ]' \
                       b'                   }' \
                       b'               ]' \
                       b'            }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

    def test_payload_execute_color_device_2(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.EXECUTE",' \
                       b'           "payload": {' \
                       b'               "commands": [' \
                       b'                   {' \
                       b'                       "execution": [' \
                       b'                           {' \
                       b'                               "command":"action.devices.commands.ColorAbsolute",' \
                       b'                               "params": {' \
                       b'                                   "color": {' \
                       b'                                       "spectrumRGB": 16510692' \
                       b'                                   }' \
                       b'                               }' \
                       b'                           }' \
                       b'                       ],' \
                       b'                       "devices": [' \
                       b'                           {' \
                       b'                               "id":"2"' \
                       b'                           }' \
                       b'                       ]' \
                       b'                   }' \
                       b'               ]' \
                       b'            }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'OK')

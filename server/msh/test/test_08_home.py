from msh import Msh
from unittest import TestCase
from webapp3 import Request
from test import read_xml


class TestHome(TestCase):

    def test_no_payload(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Questa API ha bisogno di un payload')

    def test_payload_not_json(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.body = b'dfsfs'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il payload deve essere in formato JSON')

    def test_payload_not_auth(self):
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
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'È necessario l\'header Authorization')

    def test_payload_auth_no_token(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'asfafaf'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.SYNC"' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'L\'header Authorization deve contenere un Bearer Token')

    def test_payload_auth_ko(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'Bearer dfgsdgsdg'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.SYNC"' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['output'], 'Il token fornito non è valido')

    def test_payload_sync(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'Bearer token_test'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.SYNC"' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['payload']['devices'][0]['willReportState'], True)

    def test_payload_query(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'Bearer token_test'
        request.body = b'{' \
                       b'   "requestId":"test",' \
                       b'   "inputs": [' \
                       b'       {' \
                       b'           "intent":"action.devices.QUERY",' \
                       b'           "payload": {' \
                       b'               "devices": [{' \
                       b'                   "id": "A1:FF:AA:BB:00:33"' \
                       b'               }]' \
                       b'           }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['payload']['devices']['A1:FF:AA:BB:00:33']['on'], True)

    def test_payload_execute_ok(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'Bearer token_test'
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
                       b'                               "id":"A3:FF:AA:BB:00:33"' \
                       b'                           }' \
                       b'                       ]' \
                       b'                   }' \
                       b'               ]' \
                       b'            }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['payload']['commands'][0]['status'], 'SUCCESS')

    def test_payload_execute_ko(self):
        read_xml()
        request = Request.blank('/api/home')
        request.method = 'POST'
        request.headers['Authorization'] = 'Bearer token_test'
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
                       b'                                   "on": false' \
                       b'                               }' \
                       b'                           }' \
                       b'                       ],' \
                       b'                       "devices": [' \
                       b'                           {' \
                       b'                               "id":"A1:FF:AA:BB:00:33"' \
                       b'                           }' \
                       b'                       ]' \
                       b'                   }' \
                       b'               ]' \
                       b'            }' \
                       b'       }' \
                       b'   ]' \
                       b'}'
        response = request.get_response(Msh.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['payload']['commands'][0]['status'], 'ERROR')

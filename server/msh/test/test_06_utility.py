from unittest import TestCase
from test import read_xml_prod
from module import execute_os_cmd


class TestUtility(TestCase):

    def test_execute_os_cmd_run(self):
        read_xml_prod()
        response = execute_os_cmd("pwd")
        self.assertEqual(response['return_code'], 0)
        self.assertNotEqual(response['cmd_out'], "")

    def test_execute_os_cmd_check_output(self):
        read_xml_prod()
        response = execute_os_cmd("pwd", check_out=True)
        self.assertNotEqual(response['cmd_out'], "")

    def test_execute_os_cmd_system(self):
        read_xml_prod()
        response = execute_os_cmd("pwd", sys=True)
        self.assertEqual(response, {})

from xml.dom import minidom
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class XmlReader:
    settings = {
        'string_failure': {
            'error_db': '',
            'error': ''
        }
    }
    log_mapping = {
        'debug': DEBUG,
        'info': INFO,
        'warning': WARNING,
        'error': ERROR,
        'critical': CRITICAL
    }

    def __init__(self):
        xml = minidom.parse('settings.xml')
        porta = xml.getElementsByTagName('porta')[0].firstChild.data
        lingua = xml.getElementsByTagName('lingua')[0].firstChild.data
        timestamp = xml.getElementsByTagName('timestamp')[0].firstChild.data
        ip_mode = xml.getElementsByTagName('ip_mode')[0].firstChild.data
        path = {
            'ui': xml.getElementsByTagName('path')[0].getElementsByTagName('ui')[0].firstChild.data,
            'index': xml.getElementsByTagName('path')[0].getElementsByTagName('index')[0].firstChild.data,
            'error': xml.getElementsByTagName('path')[0].getElementsByTagName('error')[0].firstChild.data,
            'db': xml.getElementsByTagName('path')[0].getElementsByTagName('db')[0].firstChild.data
        }
        log = {
            'filename': xml.getElementsByTagName('log')[0].getElementsByTagName('filename')[0].firstChild.data,
            'format': xml.getElementsByTagName('log')[0].getElementsByTagName('format')[0].firstChild.data,
            'level': XmlReader.log_mapping[xml.getElementsByTagName('log')[0].getElementsByTagName('level')[0].firstChild.data]
        }
        if log['filename'] == 'None':
            log['filename'] = None
        class_error = {
            '404': '',
            '405': ''
        }
        for elem in xml.getElementsByTagName('class_error')[0].getElementsByTagName('error'):
            class_error[elem.attributes['name'].value] = elem.firstChild.data
        shell_command = {
            'ping': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('ping')[0].firstChild.data,
            'remove': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('remove')[0].firstChild.data,
            'ifconfig': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('ifconfig')[0].firstChild.data,
            'ifconfig1': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('ifconfig1')[0].firstChild.data,
            'iwconfig': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('iwconfig')[0].firstChild.data,
            'pcwin_shutdown': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('pcwin_shutdown')[0].firstChild.data,
            'wake_on_lan': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('wake_on_lan')[0].firstChild.data,
            'net_scan': xml.getElementsByTagName('shell_command')[0].getElementsByTagName('net_scan')[0].firstChild.data
        }
        out_filename = {
            'ping': xml.getElementsByTagName('out_filename')[0].getElementsByTagName('ping')[0].firstChild.data,
            'ifconfig': xml.getElementsByTagName('out_filename')[0].getElementsByTagName('ifconfig')[0].firstChild.data,
            'pcwin_shutdown': xml.getElementsByTagName('out_filename')[0].getElementsByTagName('pcwin_shutdown')[0].firstChild.data,
            'wake_on_lan': xml.getElementsByTagName('out_filename')[0].getElementsByTagName('wake_on_lan')[0].firstChild.data,
            'net_scan': xml.getElementsByTagName('out_filename')[0].getElementsByTagName('net_scan')[0].firstChild.data
        }
        string_success = {
            'ping': xml.getElementsByTagName('string_success')[0].getElementsByTagName('ping')[0].firstChild.data,
            'pcwin_shutdown': xml.getElementsByTagName('string_success')[0].getElementsByTagName('pcwin_shutdown')[0].firstChild.data,
            'wake_on_lan': xml.getElementsByTagName('string_success')[0].getElementsByTagName('wake_on_lan')[0].firstChild.data
        }
        string_failure = {
            'open_db': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('open_db')[0].firstChild.data,
            'close_db': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('close_db')[0].firstChild.data,
            'error_db': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('error_db')[0].firstChild.data,
            'error': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('error')[0].firstChild.data,
            'generic': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('generic')[0].firstChild.data,
            'ssh_login': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('ssh_login')[0].firstChild.data,
            'no_interface': xml.getElementsByTagName('string_failure')[0].getElementsByTagName('no_interface')[0].firstChild.data
        }
        command = {
            'net': xml.getElementsByTagName('command')[0].getElementsByTagName('net')[0].firstChild.data,
            'ping': xml.getElementsByTagName('command')[0].getElementsByTagName('ping')[0].firstChild.data,
            'radio_control': xml.getElementsByTagName('command')[0].getElementsByTagName('radio_control')[0].firstChild.data,
            'radio_status': xml.getElementsByTagName('command')[0].getElementsByTagName('radio_status')[0].firstChild.data,
            'pcwin_shutdown': xml.getElementsByTagName('command')[0].getElementsByTagName('pcwin_shutdown')[0].firstChild.data,
            'wake_on_lan': xml.getElementsByTagName('command')[0].getElementsByTagName('wake_on_lan')[0].firstChild.data,
            'net_scan': xml.getElementsByTagName('command')[0].getElementsByTagName('net_scan')[0].firstChild.data
        }
        query = {
            'select_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('select_tb_net_device')[0].firstChild.data,
            'select_one_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('select_one_tb_net_device')[0].firstChild.data,
            'insert_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('insert_tb_net_device')[0].firstChild.data,
            'update_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('update_tb_net_device')[0].firstChild.data,
            'select_last_tb_net_com': xml.getElementsByTagName('query')[0].getElementsByTagName('select_last_tb_net_com')[0].firstChild.data,
            'select_tb_net_diz_cmd': xml.getElementsByTagName('query')[0].getElementsByTagName('select_tb_net_diz_cmd')[0].firstChild.data,
            'update_state_from_ip_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('update_state_from_ip_tb_net_device')[0].firstChild.data,
            'select_one_tb_res_decode': xml.getElementsByTagName('query')[0].getElementsByTagName('select_one_tb_res_decode')[0].firstChild.data
        }
        XmlReader.settings = {
            'porta': porta,
            'lingua': lingua,
            'timestamp': timestamp,
            'ip_mode': ip_mode,
            'path': path,
            'log': log,
            'class_error': class_error,
            'shell_command': shell_command,
            'out_filename': out_filename,
            'string_success': string_success,
            'string_failure': string_failure,
            'command': command,
            'query': query
        }
        return

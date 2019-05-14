from xml.dom import minidom


class XmlReader:
    settings = {}

    def __init__(self):
        xml = minidom.parse('settings.xml')
        porta = xml.getElementsByTagName('porta')[0].firstChild.data
        lingua = xml.getElementsByTagName('lingua')[0].firstChild.data
        timestamp = xml.getElementsByTagName('timestamp')[0].firstChild.data
        path = {
            'ui': xml.getElementsByTagName('path')[0].getElementsByTagName('ui')[0].firstChild.data,
            'index': xml.getElementsByTagName('path')[0].getElementsByTagName('index')[0].firstChild.data,
            'error': xml.getElementsByTagName('path')[0].getElementsByTagName('error')[0].firstChild.data,
            'db': xml.getElementsByTagName('path')[0].getElementsByTagName('db')[0].firstChild.data
        }
        log = {
            'filename': xml.getElementsByTagName('log')[0].getElementsByTagName('filename')[0].firstChild.data,
            'format': xml.getElementsByTagName('log')[0].getElementsByTagName('format')[0].firstChild.data
        }
        if log['filename'] == 'None':
            log['filename'] = None
        class_error = {
            '404': '',
            '405': ''
        }
        for elem in xml.getElementsByTagName('classError')[0].getElementsByTagName('error'):
            class_error[elem.attributes['name'].value] = elem.firstChild.data
        shell_command = {
            'ping': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('ping')[0].firstChild.data,
            'remove': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('remove')[0].firstChild.data,
            'ifconfig': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('ifconfig')[0].firstChild.data,
            'iwconfig': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('iwconfig')[0].firstChild.data,
            'pcwinShutdown': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('pcwinShutdown')[0].firstChild.data,
            'wakeOnLan': xml.getElementsByTagName('shellCommand')[0].getElementsByTagName('wakeOnLan')[0].firstChild.data
        }
        out_file = {
            'ping': xml.getElementsByTagName('outFilename')[0].getElementsByTagName('ping')[0].firstChild.data,
            'pcwinShutdown': xml.getElementsByTagName('outFilename')[0].getElementsByTagName('pcwinShutdown')[0].firstChild.data,
            'wakeOnLan': xml.getElementsByTagName('outFilename')[0].getElementsByTagName('wakeOnLan')[0].firstChild.data
        }
        string_success = {
            'ping': xml.getElementsByTagName('stringSuccess')[0].getElementsByTagName('ping')[0].firstChild.data,
            'pcwinShutdown': xml.getElementsByTagName('stringSuccess')[0].getElementsByTagName('pcwinShutdown')[0].firstChild.data,
            'wakeOnLan': xml.getElementsByTagName('stringSuccess')[0].getElementsByTagName('wakeOnLan')[0].firstChild.data
        }
        string_failure = {
            'openDB': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('openDB')[0].firstChild.data,
            'closeDB': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('closeDB')[0].firstChild.data,
            'errorDB': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('errorDB')[0].firstChild.data,
            'generic': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('generic')[0].firstChild.data,
            'sshLogin': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('sshLogin')[0].firstChild.data,
            'noInterface': xml.getElementsByTagName('stringFailure')[0].getElementsByTagName('noInterface')[0].firstChild.data
        }
        command = {
            'net': xml.getElementsByTagName('command')[0].getElementsByTagName('net')[0].firstChild.data,
            'ping': xml.getElementsByTagName('command')[0].getElementsByTagName('ping')[0].firstChild.data,
            'radioControl': xml.getElementsByTagName('command')[0].getElementsByTagName('radioControl')[0].firstChild.data,
            'radioStatus': xml.getElementsByTagName('command')[0].getElementsByTagName('radioStatus')[0].firstChild.data,
            'pcwinShutdown': xml.getElementsByTagName('command')[0].getElementsByTagName('pcwinShutdown')[0].firstChild.data,
            'wakeOnLan': xml.getElementsByTagName('command')[0].getElementsByTagName('wakeOnLan')[0].firstChild.data
        }
        query = {
            'select_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('select_tb_net_device')[0].firstChild.data,
            'select_one_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('select_one_tb_net_device')[0].firstChild.data,
            'insert_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('insert_tb_net_device')[0].firstChild.data,
            'select_last_tb_net_com': xml.getElementsByTagName('query')[0].getElementsByTagName('select_last_tb_net_com')[0].firstChild.data,
            'select_tb_net_diz_cmd': xml.getElementsByTagName('query')[0].getElementsByTagName('select_tb_net_diz_cmd')[0].firstChild.data,
            'update_state_from_ip_tb_net_device': xml.getElementsByTagName('query')[0].getElementsByTagName('update_state_from_ip_tb_net_device')[0].firstChild.data,
            'select_one_tb_res_decode':xml.getElementsByTagName('query')[0].getElementsByTagName('select_one_tb_res_decode')[0].firstChild.data
        }
        XmlReader.settings = {
            'porta': porta,
            'lingua': lingua,
            'timestamp': timestamp,
            'path': path,
            'log': log,
            'class_error': class_error,
            'shell_command': shell_command,
            'out_file': out_file,
            'string_success': string_success,
            'string_failure': string_failure,
            'command': command,
            'query': query
        }
        return

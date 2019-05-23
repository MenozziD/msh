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
        log = {
            'filename': xml.getElementsByTagName('log')[0].getElementsByTagName('filename')[0].firstChild.data,
            'format': xml.getElementsByTagName('log')[0].getElementsByTagName('format')[0].firstChild.data,
            'level': XmlReader.log_mapping[xml.getElementsByTagName('log')[0].getElementsByTagName('level')[0].firstChild.data]
        }
        if log['filename'] == 'None':
            log['filename'] = None
        XmlReader.settings = {
            'porta': porta,
            'lingua': lingua,
            'timestamp': timestamp,
            'log': log
        }
        return

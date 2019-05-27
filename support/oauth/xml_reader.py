from xml.dom import minidom
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class XmlReader:
    settings = {}
    log_mapping = {
        'debug': DEBUG,
        'info': INFO,
        'warning': WARNING,
        'error': ERROR,
        'critical': CRITICAL
    }

    def __init__(self):
        xml = minidom.parse('settings.xml')
        lingua = xml.getElementsByTagName('lingua')[0].firstChild.data
        timestamp = xml.getElementsByTagName('timestamp')[0].firstChild.data
        project_id_google_actions = xml.getElementsByTagName('project_id_google_actions')[0].firstChild.data
        log = {
            'filename': xml.getElementsByTagName('log')[0].getElementsByTagName('filename')[0].firstChild.data,
            'format': xml.getElementsByTagName('log')[0].getElementsByTagName('format')[0].firstChild.data,
            'level': XmlReader.log_mapping[xml.getElementsByTagName('log')[0].getElementsByTagName('level')[0].firstChild.data]
        }
        oauth_google = {
            'client_id': xml.getElementsByTagName('oauth_google')[0].getElementsByTagName('client_id')[0].firstChild.data,
            'client_secret': xml.getElementsByTagName('oauth_google')[0].getElementsByTagName('client_secret')[0].firstChild.data,
            'url_callback': xml.getElementsByTagName('oauth_google')[0].getElementsByTagName('url_callback')[0].firstChild.data,
        }
        if log['filename'] == 'None':
            log['filename'] = None
        XmlReader.settings = {
            'lingua': lingua,
            'timestamp': timestamp,
            'project_id_google_actions': project_id_google_actions,
            'log': log,
            'oauth_google': oauth_google
        }
        return

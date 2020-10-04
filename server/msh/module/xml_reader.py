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
    servizi_dns = ['serveo', 'pagekite']

    def __init__(self, filename):
        xml = minidom.parse(filename)
        lingua = xml.getElementsByTagName('lingua')[0].firstChild.data
        ambiente = xml.getElementsByTagName('ambiente')[0].firstChild.data
        path_db = xml.getElementsByTagName('path_db')[0].firstChild.data
        path_datastore = xml.getElementsByTagName('path_datastore')[0].firstChild.data
        timestamp = xml.getElementsByTagName('timestamp')[0].firstChild.data
        wifi_default = {
            'ssid': xml.getElementsByTagName('wifi_default')[0].getElementsByTagName('ssid')[0].firstChild.data,
            'password': xml.getElementsByTagName('wifi_default')[0].getElementsByTagName('password')[0].firstChild.data
        }
        net_on_google = xml.getElementsByTagName('net_on_google')[0].firstChild.data
        wifi_on_google = xml.getElementsByTagName('wifi_on_google')[0].firstChild.data
        project_id_google_actions = xml.getElementsByTagName('project_id_google_actions')[0].firstChild.data
        dns = {}
        for servizio in XmlReader.servizi_dns:
            servizio_json = {
                'abil': xml.getElementsByTagName('dns')[0].getElementsByTagName(servizio)[0].getElementsByTagName('abil')[0].firstChild.data,
                'test_url': xml.getElementsByTagName('dns')[0].getElementsByTagName(servizio)[0].getElementsByTagName('test_url')[0].firstChild.data,
                'domain': xml.getElementsByTagName('dns')[0].getElementsByTagName(servizio)[0].getElementsByTagName('domain')[0].firstChild.data,
                'subdomain_oauth': xml.getElementsByTagName('dns')[0].getElementsByTagName(servizio)[0].getElementsByTagName('subdomain_oauth')[0].firstChild.data,
                'subdomain_webapp': xml.getElementsByTagName('dns')[0].getElementsByTagName(servizio)[0].getElementsByTagName('subdomain_webapp')[0].firstChild.data
            }
            dns[servizio] = servizio_json
        log = {
            'filename': xml.getElementsByTagName('log')[0].getElementsByTagName('filename')[0].firstChild.data,
            'format': xml.getElementsByTagName('log')[0].getElementsByTagName('format')[0].firstChild.data,
            'level': XmlReader.log_mapping[xml.getElementsByTagName('log')[0].getElementsByTagName('level')[0].firstChild.data]
        }
        if log['filename'] == 'None':
            log['filename'] = None
        XmlReader.settings = {
            'lingua': lingua,
            'ambiente': ambiente,
            'path_db': path_db,
            'path_datastore': path_datastore,
            'timestamp': timestamp,
            'project_id_google_actions': project_id_google_actions,
            'wifi_default': wifi_default,
            'net_on_google': net_on_google,
            'wifi_on_google': wifi_on_google,
            'dns': dns,
            'log': log
        }
        print(XmlReader.settings)
        return

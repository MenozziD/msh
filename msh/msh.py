from webapp3 import WSGIApplication
from logging import basicConfig, info
from paste import httpserver
from module.utility import XmlReader
from module.net import get_ip_and_subnet
from controller.net_cmd import NetCmd
from controller.net_scan import NetScan
from controller.device_list import DeviceList
from controller.static import Index, Static, Diff, handle_error


app = WSGIApplication([
    ('/api/device_list', DeviceList),
    ('/api/net_cmd', NetCmd),
    ('/api/net_scan', NetScan),
    ('/api/diff', Diff),
    ('/', Index),
    (r'/static/(\D+)', Static),
], debug=True)
app.error_handlers[404] = handle_error
app.error_handlers[405] = handle_error
app.error_handlers[500] = handle_error


def main():
    XmlReader()
    basicConfig(
        filename=XmlReader.settings['log']['filename'],
        format=XmlReader.settings['log']['format'],
        level=XmlReader.settings['log']['level'])
    ip_address = get_ip_and_subnet()['ip']
    info("Your Computer IP Address is %s", ip_address)
    port = XmlReader.settings['porta']
    info("Server in ascolto su http://%s:%s", ip_address, port)
    httpserver.serve(app, host=ip_address, port=port)


if __name__ == '__main__':
    main()

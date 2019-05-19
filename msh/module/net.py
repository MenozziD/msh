from os import system
from pexpect import pxssh
from re import sub
from module.xml_reader import XmlReader
from logging import info, exception
from netifaces import AF_INET, gateways, ifaddresses
from urllib import request


def cmd_ping(ip, pacchetti=3):
    ping_ok = 0
    ping_err = -1
    ping_fail = 1
    file_out = XmlReader.settings['out_filename']['ping']
    result = {'ip': ip,
              'pacchetti_tx': 0,
              'pacchetti_rx': 0,
              'pacchetti_lost': 0,
              'tempo': 0,
              'result': 0,
              'cmd_output': ''
              }
    try:
        system(XmlReader.settings['shell_command']['ping'] % (str(pacchetti), ip, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system(XmlReader.settings['shell_command']['remove'] % file_out)
        result['cmd_output'] = app
        app = app.split("\n")
        app = app[len(app) - 3]
        app = app.split(", ")
        result['pacchetti_lost'] = app[2].split(" ")[0]
        result['pacchetti_tx'] = app[0].split(" ")[0]
        result['pacchetti_rx'] = app[1].split(" ")[0]
        result['tempo'] = app[3].split(" ")[1]
        if result['pacchetti_lost'] == XmlReader.settings['string_success']['ping']:
            result['result'] = ping_ok
        else:
            result['result'] = ping_fail
    except Exception as e:
        exception("Exception")
        result['result'] = ping_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_radio(ip, comando, usr, psw):
    radioctrl_err = -1
    radioctrl_invalid_cred = 2
    ss = None
    login = False
    result = {'ip': ip,
              'mac': '',
              'cmd': comando,
              'interface': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        result = cmd_radiostatus(ip, comando, usr, psw)
        if comando != 'stato' and result['interface'] != '' and result['mac'] != '':
            ss = pxssh.pxssh()
            ss.login(ip, usr, psw)
            login = True
            ss.sendline(XmlReader.settings['shell_command']['ifconfig'] % (result['interface'], result['cmd']))
            ss.prompt()
            result = cmd_radiostatus(ip, comando, usr, psw)
    except Exception as e:
        exception("Exception")
        if str(e) == "password refused":
            result['result'] = radioctrl_invalid_cred
        else:
            result['result'] = radioctrl_err
        result['cmd_output'] = str(e)
    finally:
        if login:
            ss.logout()
        return result


def cmd_radiostatus(ip, comando, usr, psw):
    radiostatus_off = 0
    radiostatus_on = 1
    radiostatus_invalid_cred = 2
    radiostatus_err = -1
    radiostatus_no_interface = -2
    ss = None
    login = False
    result = {'ip': ip,
              'mac': '',
              'cmd': comando,
              'interface': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        ss = pxssh.pxssh()
        ss.login(ip, usr, psw)
        login = True
        ss.sendline(XmlReader.settings['shell_command']['iwconfig'])
        ss.prompt()
        app = str(ss.before)[2:-1]
        result['cmd_output'] = app
        app = app.split("\\r\\n")
        for i in app:
            if i.find("ESSID:") > 0 and i.find("ESSID:\"\"") == -1:
                result['interface'] = i[:8].strip()
                result['result'] = radiostatus_on
            if i.find("Access Point:") > 0 and i.find("Access Point: Not-Associated") == -1:
                result['mac'] = i.split("Access Point: ")[1].strip()
                if not i[:8] == "        ":
                    result['interface'] = i[:8].strip()
                    result['result'] = radiostatus_off
        info("%s %s", result['interface'], result['mac'])
        if result['interface'] == '' and result['mac'] == '':
            result['result'] = radiostatus_no_interface
    except Exception as e:
        exception("Exception")
        if str(e) == "password refused":
            result['result'] = radiostatus_invalid_cred
        else:
            result['result'] = radiostatus_err
        result['cmd_output'] = str(e)
    finally:
        if login:
            ss.logout()
        return result


def cmd_pcwin_shutdown(ip, usr, psw):
    pcwin_off_ok = 0
    pcwin_off_err = -1
    pcwin_off_fail = 1
    file_out = XmlReader.settings['out_filename']['pcwin_shutdown']
    result = {'ip': ip,
              'result': 0,
              'cmd_output': ''
              }
    try:
        # user%psw
        cred = str(usr) + chr(37) + str(psw)
        system(XmlReader.settings['shell_command']['pcwin_shutdown'] % (ip, cred, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system(XmlReader.settings['shell_command']['remove'] % file_out)
        result['cmd_output'] = app
        app = sub(r'[\t\n\r]', ' ', app)
        app = app.strip()
        info(app)
        if app.find(XmlReader.settings['string_success']['pcwin_shutdown']) > 0:
            result['result'] = pcwin_off_ok
        else:
            result['result'] = pcwin_off_fail
    except Exception as e:
        exception("Exception")
        result['result'] = pcwin_off_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_wakeonlan(mac, subnet="255.255.255.255"):
    wol_ok = 0
    wol_err = -1
    wol_fail = 1
    file_out = XmlReader.settings['out_filename']['wake_on_lan']
    result = {'mac': mac,
              'subnet': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        system(XmlReader.settings['shell_command']['wake_on_lan'] % (subnet, mac, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system(XmlReader.settings['shell_command']['remove'] % file_out)
        result['cmd_output'] = app
        app = sub(r'[\t\n\r]', ' ', app)
        app = app.strip()
        info(app)
        if app.find(XmlReader.settings['string_success']['wake_on_lan']) > 0:
            result['result'] = wol_ok
        else:
            result['result'] = wol_fail
    except Exception as e:
        exception("Exception")
        result['result'] = wol_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_netscan(ip, subnet):
    netscan_ok = 0
    netscan_err = -1
    netscan_fail = 1
    count = 0
    file_out = XmlReader.settings['out_filename']['net_scan']
    result = {'result': 0,
              'devices': [],
              'cmd_output': ''
              }
    try:
        system(XmlReader.settings['shell_command']['net_scan'] % (ip, subnet, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system(XmlReader.settings['shell_command']['remove'] % file_out)
        result['cmd_output'] = app
        rows = app.split("\n")
        devices = []
        for line in rows:
            device = {'net_code': '',
                      'net_type': '',
                      'net_status': '',
                      'net_ip': '',
                      'net_mac': '',
                      'net_mac_info': ''
                      }
            if "Nmap scan report for " in line:
                line = line.replace("Nmap scan report for ", "")
                if line.find("(") < 1:
                    device['net_code'] = line.strip()
                    device['net_ip'] = line
                elif line.find("(") > 1:
                    a = line.split("(")
                    device['net_code'] = a[0].strip()
                    a[1] = a[1].replace(")", "")
                    device['net_ip'] = a[1]
                count = count + 1
            if "MAC Address" in line:
                line = line.replace("MAC Address", "")
                if line.find("(") < 1:
                    device['net_mac'] = line.strip()
                    device['net_mac_info'] = line
                elif line.find("(") > 1:
                    a = line.split("(")
                    a[0] = a[0].replace(": ", "")
                    device['net_mac'] = a[0].strip()
                    a[1] = a[1].replace(")", "")
                    device['net_mac_info'] = a[1]
            if device['net_mac'] != '' and device['net_code'] != '' and device['net_mac_info'] != '' and device['net_ip'] != '':
                devices.append(device)
                info(str(device))
        result['devices'] = devices
        if count > 0:
            result['result'] = netscan_ok
        else:
            result['result'] = netscan_fail
    except Exception as e:
        exception("Exception")
        result['result'] = netscan_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_rele(ip, command):
    url = "http://" + ip + "/cmd?n=" + command
    info("MAKE REQUEST: %s", url)
    res = request.urlopen(url)
    info("RESPOSNE: %s", res.read())


def get_ip_and_subnet():
    result = {'ip': ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['addr'],
              'subnet': ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['netmask']}
    return result

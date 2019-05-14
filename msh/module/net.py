from os import system
from pexpect import pxssh
from re import sub
from module.utility import XmlReader
import logging
import os


def cmd_ping(ip, pacchetti=5):
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
        result['result'] = ping_err
        result['cmd_output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['ping'], e)
    finally:
        return result


def cmd_radioctrl(ip, comando, usr, psw):
    radioctrl_err = -1
    radioctrl_invalid_cred = 2
    radioctrl_no_interface = -2
    no_interface = XmlReader.settings['string_failure']['no_interface']
    generic = XmlReader.settings['string_failure']['generic']
    cmd = XmlReader.settings['command']['radio_control']
    ss = None
    result = {'ip': ip,
              'mac': '',
              'cmd': comando,
              'interface': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        ss = pxssh.pxssh()
        if not ss.login(ip, usr, psw):
            result['result'] = radioctrl_invalid_cred
            raise ValueError(XmlReader.settings['string_failure']['ssh_login'] + str(ss))
        r = cmd_radiostatus(ip, usr, psw)
        if r['interface'] == '' and r['mac'] == '':
            result['result'] = radioctrl_no_interface
            raise ValueError(no_interface)
        result['interface'] = r['interface']
        ss.sendline(XmlReader.settings['shell_command']['ifconfig'] % (result['interface'], result['cmd']))
        ss.prompt()
        r = cmd_radiostatus(ip, usr, psw)
        if r['interface'] == '' and r['mac'] == '':
            result['result'] = radioctrl_no_interface
            raise ValueError(no_interface)
        result['mac'] = r['mac']
        result['result'] = r['result']
    except ValueError as v:
        result['cmd_output'] = generic % (cmd, v)
    except Exception as e:
        result['result'] = radioctrl_err
        result['cmd_output'] = generic % (cmd, e)
    finally:
        ss.logout()
        return result


def cmd_radiostatus(ip, usr, psw):
    radiostatus_off = 0
    radiostatus_on = 1
    radioctrl_invalid_cred = 2
    radiostatus_err = -1
    radiostatus_no_interface = -2
    generic = XmlReader.settings['string_failure']['generic']
    cmd = XmlReader.settings['command']['radio_status']
    ss = None
    flag_nextrow = False
    result = {'ip': ip,
              'mac': '',
              'interface': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        ss = pxssh.pxssh()
        if not ss.login(ip, usr, psw):
            result['result'] = radioctrl_invalid_cred
            raise ValueError(XmlReader.settings['string_failure']['ssh_login'] + str(ss))
        ss.sendline(XmlReader.settings['shell_command']['iwconfig'])
        ss.prompt()
        app = ss.before
        result['cmd_output'] = app
        app = sub(r'[\t\r]', ' ', app)
        app = app.split("\n")
        for i in app:
            while i.find("  ") > 0:
                i = i.replace("  ", " ")
            r = i.split(" ")
            r.remove('')
            if len(r) > 2:
                if r[1].find("no") == -1 and r[len(r)-1].find("ESSID:\"\"") == -1 and len(r[0]) > 1:
                    result['interface'] = r[0]
                    if any('Point:' in s for s in r):
                        result['mac'] = r[r.index('Point:')+1]
                        result['result'] = radiostatus_off
                    else:
                        flag_nextrow = True

                elif flag_nextrow and any('Point:' in s for s in r):
                    result['mac'] = r[r.index('Point:') + 1]
                    result['result'] = radiostatus_on
                    flag_nextrow = False

        if result['interface'] == '' and result['mac'] == '':
            result['result'] = radiostatus_no_interface
            raise ValueError(XmlReader.settings['string_failure']['no_interface'])
    except ValueError as v:
        result['cmd_output'] = generic % (cmd, v)
    except Exception as e:
        result['result'] = radiostatus_err
        result['cmd_output'] = generic % (cmd, e)
    finally:
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
        logging.info(app)
        if app.find(XmlReader.settings['string_success']['pcwin_shutdown']):
            result['result'] = pcwin_off_ok
        else:
            result['result'] = pcwin_off_fail
    except Exception as e:
        result['result'] = pcwin_off_err
        result['cmd_output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['pcwin_shutdown'], e)
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
        logging.info(app)
        if app.find(XmlReader.settings['string_success']['wake_on_lan']):
            result['result'] = wol_ok
        else:
            result['result'] = wol_fail
    except Exception as e:
        result['result'] = wol_err
        result['cmd_output'] = XmlReader.settings['string_failure']['generic'] % (XmlReader.settings['command']['wake_on_lan'], e)
    finally:
        return result


def cmd_netscan():
    netscan_ok = 0
    netscan_err = -1
    netscan_fail = 1
    count = 0

    file_out = XmlReader.settings['out_filename']['net_scan']

    result = {'result': 0,
              'devices': [],
              'cmd_output': ''
              }
    device = {'net_code': '',
              'net_type': '',
              'net_status': '',
              'net_ip': '',
              'net_mac': '',
              'net_mac_info': ''
              }
    try:
        system(XmlReader.settings['shell_command']['net_scan'] % file_out)
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system(XmlReader.settings['shell_command']['remove'] % file_out)
        result['cmd_output'] = app
        logging.info(app)
        rows = app.split("\n")
        for line in rows:

            if "Nmap scan report for " in line:
                line = line.replace("Nmap scan report for ", "")
                if line.find("(") < 1:
                    device['net_code'] = line
                    device['net_ip'] = line
                elif line.find("(") > 1:
                    a = line.split("(")
                    device['net_code'] = a[0]
                    a[1] = a[1].replace(")", "")
                    device['net_ip'] = a[1]

                count = count + 1

            if "MAC Address" in line:
                line = line.replace("MAC Address", "")
                if line.find("(") < 1:
                    device['net_mac'] = line
                    device['net_mac_info'] = line
                elif line.find("(") > 1:
                    a = line.split("(")
                    a[0] = a[0].replace(": ", "")
                    device['net_mac'] = a[0]
                    a[1] = a[1].replace(")", "")
                    device['net_mac_info'] = a[1]

            if device['net_mac'] != '' and device['net_code'] != '' and device['net_mac_info'] != '' and device['net_ip'] != '':
                result['devices'].append(device)
                logging.info(str(device))
                device = {'net_code': '',
                          'net_type': '',
                          'net_status': '',
                          'net_ip': '',
                          'net_mac': '',
                          'net_mac_info': ''
                          }

        if count > 0:
            result['result']= netscan_ok
        else:
            result['result'] = netscan_fail

    except  Exception as e:
        result['result'] = netscan_err
        result['cmd_output'] = XmlReader.settings['string_failure']['generic'] % ( XmlReader.settings['command']['net_scan'], e)

    finally:
        return result

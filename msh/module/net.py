from pexpect import pxssh
from logging import info, exception
from netifaces import AF_INET, gateways, ifaddresses
from json import loads
from urllib import request
from subprocess import run, PIPE


def cmd_ping(ip, pacchetti=3):
    ping_ok = 0
    ping_err = -1
    ping_fail = 1
    result = {
        'ip': ip,
        'pacchetti_tx': 0,
        'pacchetti_rx': 0,
        'pacchetti_lost': 0,
        'tempo': 0,
        'result': 0,
        'cmd_output': ''
    }
    try:
        cmd = run(['ping', '-c', str(pacchetti), ip], stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1].replace("\\n", "\n")
        cmd_err = str(cmd.stderr)[2:-1].replace("\\n", "\n")
        if cmd_out != "":
            result['cmd_output'] = cmd_out
            cmd_out = cmd_out.split("\n")
            cmd_out = cmd_out[len(cmd_out) - 3].split(", ")
            result['pacchetti_lost'] = cmd_out[2].split(" ")[0]
            result['pacchetti_tx'] = cmd_out[0].split(" ")[0]
            result['pacchetti_rx'] = cmd_out[1].split(" ")[0]
            result['tempo'] = cmd_out[3].split(" ")[1]
            if result['pacchetti_lost'] == '0%':
                result['result'] = ping_ok
            else:
                result['result'] = ping_fail
        else:
            result['cmd_output'] = cmd_err
            result['result'] = ping_err
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
    command = "ifconfig %s %s"
    result = {
        'ip': ip,
        'mac': '',
        'cmd': comando,
        'interface': '',
        'result': 0,
        'cmd_output': ''
    }
    try:
        result = cmd_radio_stato(ip, comando, usr, psw)
        if comando != 'stato' and result['interface'] != '' and result['mac'] != '':
            ss = pxssh.pxssh()
            ss.login(ip, usr, psw)
            login = True
            ss.sendline(command % (result['interface'], result['cmd']))
            ss.prompt()
            result = cmd_radio_stato(ip, comando, usr, psw)
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


def cmd_radio_stato(ip, comando, usr, psw):
    radiostatus_off = 0
    radiostatus_on = 1
    radiostatus_invalid_cred = 2
    radiostatus_err = -1
    radiostatus_no_interface = -2
    ss = None
    login = False
    command = "iwconfig"
    result = {
        'ip': ip,
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
        ss.sendline(command)
        ss.prompt()
        cmd_out = str(ss.before)[2:-1].replace("\\r\\n", '\r\n')
        result['cmd_output'] = cmd_out
        cmd_out = cmd_out.split("\r\n")
        for row in cmd_out:
            if row.find("ESSID:") > 0 and row.find("ESSID:\"\"") == -1:
                result['interface'] = row[:8].strip()
                result['result'] = radiostatus_on
            if row.find("Access Point:") > 0 and row.find("Access Point: Not-Associated") == -1:
                result['mac'] = row.split("Access Point: ")[1].strip()
                if not row[:8] == "        ":
                    result['interface'] = row[:8].strip()
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
    result = {
        'ip': ip,
        'result': 0,
        'cmd_output': ''
    }
    try:
        # user%psw
        cmd = run(['net', 'rcp', '-I', ip, '-U', str(usr) + chr(37) + str(psw)], stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
        cmd_err = str(cmd.stderr)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
        if cmd_out != "":
            result['cmd_output'] = cmd_out
            cmd_out = cmd_out.replace("\t", "").replace("\n", "")
            cmd_out = cmd_out.strip()
            if cmd_out.find('succeeded') > 0:
                result['result'] = pcwin_off_ok
            else:
                result['result'] = pcwin_off_fail
        else:
            result['cmd_output'] = cmd_err
            result['result'] = pcwin_off_err
    except Exception as e:
        exception("Exception")
        result['result'] = pcwin_off_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_wakeonlan(mac):
    wol_ok = 0
    wol_err = -1
    wol_fail = 1
    result = {
        'mac': mac,
        'result': 0,
        'cmd_output': ''
    }
    try:
        cmd = run(['wakeonlan', mac], stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
        cmd_err = str(cmd.stderr)[2:-1].replace("\\t", "\t").replace("\\n", "\n")
        if cmd_out != "":
            result['cmd_output'] = cmd_out
            cmd_out = cmd_out.replace("\t", "").replace("\n", "")
            cmd_out = cmd_out.strip()
            if cmd_out.find('Sending magic packet') >= 0:
                result['result'] = wol_ok
            else:
                result['result'] = wol_fail
        else:
            result['cmd_output'] = cmd_err
            result['result'] = wol_err
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
    result = {
        'result': 0,
        'devices': [],
        'cmd_output': ''
    }
    try:
        cmd = run(['sudo', 'nmap', '-sn', ip + "/" + subnet], stdout=PIPE, stderr=PIPE)
        cmd_out = str(cmd.stdout)[2:-1].replace("\\n", "\n")
        cmd_err = str(cmd.stderr)[2:-1].replace("\\n", "\n")
        if cmd_out != "":
            result['cmd_output'] = cmd_out
            rows = cmd_out.split("\n")
            devices = []
            device = {
                'net_code': '',
                'net_ip': '',
                'net_mac': '',
                'net_mac_info': ''
            }
            for line in rows:
                if "Nmap scan report for " in line:
                    line = line.replace("Nmap scan report for ", "")
                    if line.find("(") > 0:
                        device['net_code'] = line.split(" (")[0]
                        device['net_ip'] = line.split(" (")[1].replace(")", "")
                    else:
                        device['net_ip'] = line
                        device['net_code'] = line
                if "MAC Address" in line:
                    line = line.replace("MAC Address: ", "")
                    device['net_mac'] = line.split(" (")[0]
                    device['net_mac_info'] = line.split(" (")[1].replace(")", "")
                    if device['net_mac_info'] == 'Unknown':
                        url = 'https://api.macvendors.com/' + device['net_mac']
                        info("MAKE REQUEST: %s", url)
                        response = request.urlopen(url).read()
                        info("RESPONSE: %s", response)
                        device['net_mac_info'] = response
                if device['net_mac'] != '' and device['net_code'] != '' and device['net_mac_info'] != '' and device['net_ip'] != '':
                    devices.append(device)
                    device = {
                        'net_code': '',
                        'net_ip': '',
                        'net_mac': '',
                        'net_mac_info': ''
                    }
            result['devices'] = devices
            if len(devices) > 0:
                result['result'] = netscan_ok
            else:
                result['result'] = netscan_fail
        else:
            result['cmd_output'] = cmd_err
            result['result'] = netscan_err
    except Exception as e:
        exception("Exception")
        result['result'] = netscan_err
        result['cmd_output'] = str(e)
    finally:
        return result


def cmd_rele(ip, command):
    esp_on = 0
    esp_off = 1
    esp_err = -1
    url = "http://" + ip + "/cmd?n=" + command
    info("MAKE REQUEST: %s", url)
    result = {
        'url_request': url
    }
    try:
        response = loads(request.urlopen(url).read().decode('utf-8'))
        info("RESPONSE: %s", response)
        result['cmd_output'] = response
        esp_decode = {
            'ON': esp_on,
            'OFF': esp_off,
            'ERR': esp_err,
        }
        result['result'] = esp_decode[response['output']]
    except Exception as e:
        exception("Exception")
        result['result'] = esp_err
        result['cmd_output'] = str(e)
    return result


def get_ip_and_subnet():
    result = {
        'ip': ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['addr'],
        'subnet': ifaddresses(gateways()['default'][AF_INET][1])[AF_INET][0]['netmask']
    }
    return result

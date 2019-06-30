from pexpect import pxssh
from logging import info, exception
from json import loads
from urllib import request
from time import sleep
from module import execute_os_cmd


def cmd_ping(ip, pacchetti=3):
    ping_ok = 0
    ping_exception = -1
    ping_fail = 1
    result = {}
    try:
        result['ip'] = ip
        cmd = 'ping -c %s %s' % (str(pacchetti), ip)
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            result['cmd_output'] = response['cmd_out']
            cmd_out = response['cmd_out'].split('ping statistics ---\n')[1]
            result['pacchetti_lost'] = cmd_out.split(" packet loss,")[0].split("received, ")[1]
            result['pacchetti_tx'] = cmd_out.split(" packets transmitted")[0]
            result['pacchetti_rx'] = cmd_out.split(" received,")[0].split(", ")[1]
            result['tempo'] = cmd_out.split(", time ")[1].split("\n")[0]
            if result['pacchetti_lost'] == '0%':
                result['result'] = ping_ok
            else:
                result['result'] = ping_fail
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = ping_exception
        result['output'] = str(e)
    finally:
        return result


def cmd_radio(ip, comando, usr, psw):
    radioctrl_exception = -1
    ss = None
    login = False
    result = {}
    try:
        result = cmd_radio_stato(ip, comando, usr, psw)
        if comando != 'stato' and result['interface'] != '' and result['mac'] != '':
            ss = pxssh.pxssh()
            ss.login(ip, usr, psw)
            login = True
            cmd = "ifconfig %s %s" % (result['interface'], result['cmd'])
            info("Eseguo comando in SSH: %s", cmd)
            ss.sendline(cmd)
            ss.prompt()
            result = cmd_radio_stato(ip, comando, usr, psw)
    except Exception as e:
        exception("Exception")
        result['result'] = radioctrl_exception
        result['output'] = str(e)
    finally:
        if login:
            ss.logout()
        return result


def cmd_radio_stato(ip, comando, usr, psw):
    radiostatus_invalid_cred = 2
    radiostatus_exception = -1
    radiostatus_no_interface = -2
    ss = None
    login = False
    result = {}
    try:
        result = {
            'ip': ip,
            'cmd': comando,
        }
        ss = pxssh.pxssh()
        ss.login(ip, usr, psw)
        login = True
        cmd = "iwconfig"
        info("Eseguo comando in SSH: %s", cmd)
        ss.sendline(cmd)
        ss.prompt()
        cmd_out = str(ss.before)[2:-1].replace("\\r\\n", '\r\n')
        result['cmd_output'] = cmd_out
        cmd_out = cmd_out.split("\r\n")
        for row in cmd_out:
            result = read_essid(row, result)
            result = read_mac(row, result)
        info("INTERFACE: %s MAC: %s", result['interface'], result['mac'])
        if result['interface'] == '' and result['mac'] == '':
            result['result'] = radiostatus_no_interface
        result['output'] = 'OK'
    except Exception as e:
        exception("Exception")
        if str(e) == "password refused":
            result['result'] = radiostatus_invalid_cred
        else:
            result['result'] = radiostatus_exception
        result['output'] = str(e)
    finally:
        if login:
            ss.logout()
        return result


def read_essid(row, result):
    radiostatus_on = 1
    if row.find("ESSID:") > 0 and row.find("ESSID:\"\"") == -1:
        result['interface'] = row[:8].strip()
        result['result'] = radiostatus_on
    return result


def read_mac(row, result):
    radiostatus_off = 0
    if row.find("Access Point:") > 0 and row.find("Access Point: Not-Associated") == -1:
        result['mac'] = row.split("Access Point: ")[1].strip()
        if not row[:8] == "        ":
            result['interface'] = row[:8].strip()
            result['result'] = radiostatus_off
    return result


def cmd_pcwin_shutdown(ip, usr, psw):
    pcwin_off_ok = 0
    pcwin_off_exception = -1
    pcwin_off_fail = 1
    result = {
        'ip': ip,
        'result': 0,
        'cmd_output': ''
    }
    try:
        # user%psw
        cmd = 'net rcp -I %s -U %s' % (ip, usr + '%' + psw)
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            result['cmd_output'] = response['cmd_out']
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find('succeeded') > 0:
                result['result'] = pcwin_off_ok
            else:
                result['result'] = pcwin_off_fail
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = pcwin_off_exception
        result['output'] = str(e)
    finally:
        return result


def cmd_wakeonlan(mac):
    wol_ok = 0
    wol_fail = 1
    wol_exception = -1
    result = {}
    try:
        result['mac'] = mac
        cmd = 'wakeonlan %s' % mac
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            result['cmd_output'] = response['cmd_out']
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find('Sending magic packet') >= 0:
                result['result'] = wol_ok
            else:
                result['result'] = wol_fail
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = wol_exception
        result['output'] = str(e)
    finally:
        return result


def cmd_netscan(ip, subnet):
    netscan_ok = 0
    netscan_exception = 2
    result = {}
    try:
        cmd = "sudo nmap -sn %s/%s" % (ip, subnet)
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            result['cmd_output'] = response['cmd_out']
            rows = response['cmd_out'].split("\n")
            devices = []
            device = {
                'net_code': '',
                'net_ip': '',
                'net_mac': '',
                'net_mac_info': ''
            }
            for line in rows:
                device = get_code_and_ip(line, device)
                if "MAC Address" in line:
                    line = line.replace("MAC Address: ", "")
                    device['net_mac'] = line.split(" (")[0]
                    device['net_mac_info'] = line.split(" (")[1].replace(")", "")
                    device = get_mac_info(device)
                if device['net_mac'] != '' and device['net_code'] != '' and device['net_mac_info'] != '' and device['net_ip'] != '':
                    devices.append(device)
                    device = {
                        'net_code': '',
                        'net_ip': '',
                        'net_mac': '',
                        'net_mac_info': ''
                    }
            result['devices'] = devices
            result['result'] = netscan_ok
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = netscan_exception
        result['output'] = str(e)
    finally:
        return result


def get_code_and_ip(line, device):
    if "Nmap scan report for " in line:
        line = line.replace("Nmap scan report for ", "")
        if line.find("(") > 0:
            device['net_code'] = line.split(" (")[0]
            device['net_ip'] = line.split(" (")[1].replace(")", "")
        else:
            device['net_ip'] = line
            device['net_code'] = line
    return device


def get_mac_info(device):
    if device['net_mac_info'] == 'Unknown':
        url = 'https://api.macvendors.com/' + device['net_mac']
        finito = False
        while not finito:
            try:
                info("MAKE REQUEST: %s", url)
                response = str(request.urlopen(url).read())
                if response.find('b\'') == 0:
                    response = response[2:-1]
                info("RESPONSE: %s", response)
                device['net_mac_info'] = response
                finito = True
                sleep(2)
            except Exception:
                exception("Exception")
                sleep(2)
    return device


def cmd_esp(ip, command):
    esp_on = 0
    esp_off = 1
    esp_err = -1
    esp_exception = 2
    result = {}
    try:
        url = "http://" + ip + "/cmd?n=" + command
        info("MAKE REQUEST: %s", url)
        result['url_request'] = url
        response = loads(request.urlopen(url).read().decode('utf-8'))
        info("RESPONSE: %s", response)
        esp_decode = {
            'ON': esp_on,
            'OFF': esp_off,
            'ERR': esp_err,
        }
        result['output'] = 'OK'
        result['result'] = esp_decode[response['output']]
        result['cmd_output'] = response
    except Exception as e:
        exception("Exception")
        result['result'] = esp_exception
        result['output'] = str(e)
    finally:
        return result


def compile_arduino(core, tipologia):
    result = {}
    compile_ok = 1
    compile_ko = 2
    try:
        cmd = 'mkdir %s' % tipologia
        execute_os_cmd(cmd)
        url_repo_device = 'https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/%s' % tipologia
        cmd = 'curl %s/%s.ino --output %s/%s.ino' % (url_repo_device, tipologia, tipologia, tipologia)
        execute_os_cmd(cmd)
        cmd = 'curl %s/index.h --output %s/index.h' % (url_repo_device, tipologia)
        execute_os_cmd(cmd)
        cmd = "arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'"
        info("Eseguo comando: %s", cmd)
        fqbn = execute_os_cmd(cmd, check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        cmd_compile = 'sudo arduino-cli compile --fqbn %s %s' % (fqbn, tipologia)
        response = execute_os_cmd(cmd_compile)
        if response['cmd_err'] == '':
            cmd_out_split = response['cmd_out'].split('\n')
            program_info = cmd_out_split[-3]
            memory_info = cmd_out_split[-2]
            compile_output = {
                'program_bytes_used': program_info.split("uses ")[1].split(" bytes")[0],
                'program_percentual_used': program_info.split("(")[1].split(")")[0],
                'program_bytes_total': program_info.split("Maximum is ")[1].split(" bytes")[0],
                'memory_bytes_used': memory_info.split("use ")[1].split(" bytes")[0],
                'memory_percentual_used': memory_info.split("(")[1].split(")")[0],
                'memory_bytes_free': memory_info.split("leaving ")[1].split(" bytes")[0],
                'memory_bytes_total': memory_info.split("Maximum is ")[1].split(" bytes")[0]
            }
            result['compile_output'] = compile_output
            result['result'] = compile_ok
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = compile_ko
        result['output'] = str(e)
    finally:
        return result


def upload_arduino(core, tipologia):
    upload_ko = 1
    upload_ok = 2
    result = {}
    try:
        cmd = "arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'"
        info("Eseguo comando: %s", cmd)
        fqbn = execute_os_cmd(cmd, check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        cmd = "arduino-cli board list | grep tty | awk '{print $1}'"
        usb = execute_os_cmd(cmd, check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        info("USB: %s", usb)
        if usb != "":
            cmd_upload = 'sudo arduino-cli upload -p %s --fqbn %s %s' % (usb, fqbn, tipologia)
            response = execute_os_cmd(cmd_upload)
            if response['cmd_err'] == "":
                cmd_out = response['cmd_out'].replace("\\r", "")
                upload_output = {
                    'porta_seriale': cmd_out.split("Serial port ")[1].split("\n")[0],
                    'chip': cmd_out.split("Chip is ")[1].split("\n")[0],
                    'mac_addres': cmd_out.split("MAC: ")[1].split("\n")[0],
                    'byte_write': cmd_out.split("Wrote ")[1].split(" bytes")[0],
                    'byte_write_compressed': cmd_out.split("Wrote ")[1].split(" compressed)")[0].split("(")[0],
                    'time': cmd_out.split(" (effective")[0].split("compressed) at ")[1].split(" in ")[1]
                }
                result['upload_output'] = upload_output
                result['result'] = upload_ok
                result['output'] = 'OK'
            else:
                raise Exception(response['cmd_err'])
        else:
            raise Exception('Nessun dispositivo collegato')
    except Exception as e:
        exception("Exception")
        result['result'] = upload_ko
        result['output'] = str(e)
    finally:
        return result

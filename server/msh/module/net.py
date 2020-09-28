from logging import info, exception
from json import loads
from time import sleep
from fritzconnection import FritzConnection
from module import execute_os_cmd, execute_ssh_cmd, execute_request_http, get_string, DbManager


def cmd_ping(ip, pacchetti=1):
    result = {}
    try:
        result['ip'] = ip
        response = execute_os_cmd('ping -c %s %s' % (str(pacchetti), ip))
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].split('ping statistics ---\n')[1]
            result['pacchetti_lost'] = cmd_out.split(" packet loss,")[0].split("received, ")[1]
            result['pacchetti_tx'] = cmd_out.split(" packets transmitted")[0]
            result['pacchetti_rx'] = cmd_out.split(" received,")[0].split(", ")[1]
            result['tempo'] = cmd_out.split(", time ")[1].split("\n")[0]
            if result['pacchetti_lost'] == '0%':
                result['result'] = get_string(0)
            else:
                result['result'] = get_string(1)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(2)
        result['output'] = str(e)
    finally:
        return result


def cmd_radio(ip, comando, usr, psw):
    result = {}
    try:
        result = cmd_radio_stato(ip, usr, psw)
        if comando != 'stato' and result['output'] == 'OK' and 'interface' in result and 'mac' in result:
            execute_ssh_cmd(ip, usr, psw, "ifconfig %s %s" % (result['interface'], comando))
            result['result'] = get_string(9)
            result['output'] = 'OK'
        else:
            if result['output'] != 'OK':
                raise Exception(result['output'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(14)
        result['output'] = str(e)
    finally:
        return result


def cmd_radio_stato(ip, usr, psw):
    result = {}
    try:
        response = execute_ssh_cmd(ip, usr, psw, "iwconfig")
        if response['output'] == 'OK':
            cmd_out = response['cmd_out'].split("\r\n")
            for row in cmd_out:
                result = read_essid(row, result)
                result = read_mac(row, result)
            if 'mac' in result:
                info("INTERFACE: %s MAC: %s", result['interface'], result['mac'])
            else:
                raise Exception(get_string(12))
            result['output'] = 'OK'
        else:
            raise Exception(response['output'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(14)
        result['output'] = str(e)
    finally:
        return result


def read_essid(row, result):
    if row.find("ESSID:") > 0 and row.find("ESSID:\"\"") == -1:
        result['ssid'] = row.split("ESSID:\"")[1].split("\"")[0]
        result['interface'] = row[:8].strip()
        result['result'] = get_string(0)
        info("SSID: %s ", result['ssid'])
    return result


def read_mac(row, result):
    if row.find("Access Point:") > 0 and row.find("Access Point: Not-Associated") == -1:
        result['mac'] = row.split("Access Point: ")[1].strip()
        if not row[:8] == "        ":
            result['interface'] = row[:8].strip()
            result['result'] = get_string(1)
    return result


def cmd_pc(comando, mac=None, ip=None, usr=None, psw=None, cmd_str="", ok_str=""):
    if comando == 'on':
        result = cmd_wakeonlan(mac)
    else:
        result = cmd_shutdown(ip, usr, psw, cmd_str, ok_str)
    return result


def cmd_shutdown(ip, usr, psw, cmd_str, ok_str):
    result = {}
    try:
        # user%psw
        response = execute_ssh_cmd(ip, usr, psw, cmd_str)
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find(ok_str) >= 0:
                result['result'] = get_string(6)
            else:
                result['result'] = get_string(7)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(8)
        result['output'] = str(e)
    finally:
        return result


def cmd_wakeonlan(mac):
    result = {}
    try:
        result['mac'] = mac
        response = execute_os_cmd('wakeonlan %s' % mac)
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find('Sending magic packet') >= 0:
                result['result'] = get_string(3)
            else:
                result['result'] = get_string(4)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(5)
        result['output'] = str(e)
    finally:
        return result


def cmd_netscan(ip, subnet):
    result = {}
    try:
        response = execute_os_cmd("sudo nmap -sn %s/%s" % (ip, subnet))
        if response['cmd_err'] == "":
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
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
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
        response = execute_request_http(url)
        if response.find('b\'') == 0:
            response = response[2:-1]
        device['net_mac_info'] = response
        sleep(2)
    return device


def cmd_esp(ip, command):
    result = {}
    try:
        url = "http://" + ip + "/cmd?n=" + command
        result['url_request'] = url
        response = loads(execute_request_http(url))
        result['output'] = 'OK'
        if response['output'].find("ERR") == 0:
            sleep(2)
            response = loads(execute_request_http(url))
            result['result'] = response['output']
        else:
            result['result'] = response['output']
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(16)
        result['output'] = str(e)
    finally:
        return result


def compile_arduino(core, tipologia):
    result = {}
    try:
        execute_os_cmd('mkdir %s' % tipologia)
        url_repo_device = 'https://raw.githubusercontent.com/VanMenoz92/msh/master/devices/%s' % tipologia
        cmd = 'curl %s/%s.ino --output %s/%s.ino' % (url_repo_device, tipologia, tipologia, tipologia)
        execute_os_cmd(cmd)
        execute_os_cmd('curl %s/index.h --output %s/index.h' % (url_repo_device, tipologia))
        set_arduino_wifi_set(tipologia)
        fqbn = execute_os_cmd("arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'", check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        response = execute_os_cmd('sudo arduino-cli compile --fqbn %s %s' % (fqbn, tipologia))
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
            result['result'] = get_string(17)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(18)
        result['output'] = str(e)
    finally:
        return result


def set_arduino_wifi_set(tipologia):
    try:
        ret_wifi = DbManager.select_tb_wifi()
        file_name = "%s/%s.ino" % (tipologia, tipologia)
        f = open(file_name, "r")
        source_code = f.read()
        f.close()
        source_code = source_code.replace("#define STASSID \"\"", "#define STASSID \"%s\"" % ret_wifi[0]['ssid'])
        source_code = source_code.replace("#define STAPSK \"\"", "#define STAPSK \"%s\"" % ret_wifi[0]['psw'])
        f = open(file_name, "w")
        f.write(source_code)
        f.close()
    except Exception as e:
        exception("Exception")


def upload_arduino(core, tipologia):
    result = {}
    try:
        fqbn = execute_os_cmd("arduino-cli board listall | grep \"" + core + "\" | awk '{print $NF}'", check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        usb = execute_os_cmd("arduino-cli board list | grep tty | awk '{print $1}'", check_out=True)['cmd_out'].replace("\n", "").replace("\t", "")
        info("USB: %s", usb)
        if usb != "":
            response = execute_os_cmd('sudo arduino-cli upload -p %s --fqbn %s %s' % (usb, fqbn, tipologia))
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
                result['result'] = get_string(19)
                result['output'] = 'OK'
            else:
                raise Exception(response['cmd_err'])
        else:
            raise Exception(get_string(38))
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(20)
        result['output'] = str(e)
    finally:
        return result


def wifi_ap_info(ip, usr, psw, router):
    result = {}
    wifi_ap = []
    try:
        if usr != '':
            response = execute_ssh_cmd(ip, usr, psw, "cat /etc/config/wireless")
            if response['output'] == 'OK':
                wifi_info = {
                    'router': router,
                    'psw_type': 'WPA/PSK2'
                }
                if response['cmd_out'].find("No such file or directory") > 0:
                    response = execute_ssh_cmd(ip, usr, psw, "cd /etc/Wireless && cd `ls` && cat `ls`")
                    if response['output'] == 'OK':
                        cmd_out = response['cmd_out'].replace("\\t", "").replace("\\r", "").replace("\r", "").replace("\\n", "\n")
                        rows = cmd_out.split('\n')
                        for row in rows:
                            wifi_info = get_field_asus(row, wifi_info, 'SSID', 'ssid', 5)
                            wifi_info = get_field_asus(row, wifi_info, 'WPAPSK', 'wpa_psk_key', 7)
                            if 'ssid' in wifi_info and 'wpa_psk_key' in wifi_info:
                                wifi_ap.append(wifi_info)
                                wifi_info = {
                                    'router': router,
                                    'psw_type': 'WPA/PSK2'
                                }
                    else:
                        raise Exception(response['output'])
                else:
                    cmd_out = response['cmd_out'].replace("\\t", "").replace("\\n", "\n").replace("\\r", "")
                    rows = cmd_out.split('config')
                    for row in rows:
                        wifi_info = get_field(row, wifi_info, 'ssid')
                        wifi_info = get_field(row, wifi_info, 'wpa_psk_key')
                        if 'ssid' in wifi_info and 'wpa_psk_key' in wifi_info:
                            wifi_ap.append(wifi_info)
                            wifi_info = {
                                'router': router,
                                'psw_type': 'WPA/PSK2'
                            }
            else:
                raise Exception(response['output'])
        else:
            fc = FritzConnection(address=ip, password=psw)
            info(fc.call_action('WLANConfiguration1', 'GetInfo')['NewSSID'])
            wifi_info = {
                'router': router,
                'psw_type': 'WPA/PSK2',
                'ssid': fc.call_action('WLANConfiguration1', 'GetInfo')['NewSSID'],
                'wpa_psk_key': ''
            }
            wifi_ap.append(wifi_info)
        result['result'] = wifi_ap
        info(wifi_ap)
        result['output'] = "OK"
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(42)
        result['output'] = str(e)
    finally:
        return result


def get_field(row, wifi_info, field):
    if row.find('option ' + field + ' \'') > -1:
        wifi_info[field] = row.split('option ' + field + ' \'')[1].split("\'")[0]
    return wifi_info


def get_field_asus(row, wifi_info, field, tag, size):
    if row.find(field) > -1:
        if len(row.split('=')) == 2 and len(row.split('=')[0]) == size and row.split('=')[1] != "":
            wifi_info[tag] = row.split('=')[1]
    return wifi_info


def cmd_ps4(cmd):
    result = {}
    base = "sudo ps4-waker"
    try:
        response = execute_os_cmd(base + " check")
        if response['cmd_err'] == '':
            ps4_check = loads(response['cmd_out'])
            if cmd == 'toggle':
                if ps4_check['status'] == 'Standby':
                    response = execute_os_cmd(base)
                else:
                    response = execute_os_cmd(base + " standby")
                result['result'] = get_string(43)
                if response['cmd_err'] == '':
                    result['output'] = "OK"
                else:
                    raise Exception(response['cmd_err'])
            else:
                if ps4_check['status'] == 'Standby':
                    result['result'] = 'OFF'
                else:
                    result['result'] = 'ON'
                result['output'] = "OK"
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(44)
        result['output'] = str(e)
    finally:
        return result


def cmd_reboot(ip, usr, psw):
    result = {}
    try:
        response = execute_ssh_cmd(ip, usr, psw, "reboot")
        if response['output'] == 'OK':
            result['result'] = 'OK'
            result['output'] = 'OK'
        else:
            raise Exception(response['output'])
    except Exception as e:
        exception("Exception")
        result['result'] = get_string(14)
        result['output'] = str(e)
    finally:
        return result

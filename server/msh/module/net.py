from logging import info, exception
from json import loads
from time import sleep
from module import execute_os_cmd, execute_ssh_cmd, execute_request_http, DbManager, XmlReader


def cmd_ping(ip, pacchetti=1):
    result = {}
    try:
        result['ip'] = ip
        cmd = 'ping -c %s %s' % (str(pacchetti), ip)
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].split('ping statistics ---\n')[1]
            result['pacchetti_lost'] = cmd_out.split(" packet loss,")[0].split("received, ")[1]
            result['pacchetti_tx'] = cmd_out.split(" packets transmitted")[0]
            result['pacchetti_rx'] = cmd_out.split(" received,")[0].split(", ")[1]
            result['tempo'] = cmd_out.split(", time ")[1].split("\n")[0]
            if result['pacchetti_lost'] == '0%':
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 0)
            else:
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 1)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 2)
        result['output'] = str(e)
    finally:
        return result


def cmd_radio(ip, comando, usr, psw):
    result = {}
    try:
        result = cmd_radio_stato(ip, usr, psw)
        if comando != 'stato' and result['output'] == 'OK' and 'interface' in result and 'mac' in result:
            cmd = "ifconfig %s %s" % (result['interface'], comando)
            execute_ssh_cmd(ip, usr, psw, cmd)
            result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 9)
            result['output'] = 'OK'
        else:
            if result['output'] != 'OK':
                raise Exception(result['output'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 14)
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
            if 'interface' not in result and 'mac' not in result:
                raise Exception(DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 12))
            else:
                info("INTERFACE: %s MAC: %s", result['interface'], result['mac'])
                result['output'] = 'OK'
        else:
            raise Exception(response['output'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 14)
        result['output'] = str(e)
    finally:
        return result


def read_essid(row, result):
    if row.find("ESSID:") > 0 and row.find("ESSID:\"\"") == -1:
        result['interface'] = row[:8].strip()
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 10)
    return result


def read_mac(row, result):
    if row.find("Access Point:") > 0 and row.find("Access Point: Not-Associated") == -1:
        result['mac'] = row.split("Access Point: ")[1].strip()
        if not row[:8] == "        ":
            result['interface'] = row[:8].strip()
            result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 11)
    return result


def cmd_pcwin_shutdown(ip, usr, psw):
    result = {}
    try:
        # user%psw
        cmd = 'net rcp -I %s -U %s' % (ip, usr + '%' + psw)
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find('succeeded') > 0:
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 6)
            else:
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 7)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 8)
        result['output'] = str(e)
    finally:
        return result


def cmd_wakeonlan(mac):
    result = {}
    try:
        result['mac'] = mac
        cmd = 'wakeonlan %s' % mac
        response = execute_os_cmd(cmd)
        if response['cmd_err'] == "":
            cmd_out = response['cmd_out'].replace("\t", "").replace("\n", "").strip()
            if cmd_out.find('Sending magic packet') >= 0:
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 3)
            else:
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 4)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 5)
        result['output'] = str(e)
    finally:
        return result


def cmd_netscan(ip, subnet):
    result = {}
    try:
        cmd = "sudo nmap -sn %s/%s" % (ip, subnet)
        response = execute_os_cmd(cmd)
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
        esp_decode = {
            'ON': DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 15),
            'OFF': DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 15),
            'ERR': DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 16),
        }
        result['output'] = 'OK'
        result['result'] = esp_decode[response['output']]
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 16)
        result['output'] = str(e)
    finally:
        return result


def compile_arduino(core, tipologia):
    result = {}
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
            result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 17)
            result['output'] = 'OK'
        else:
            raise Exception(response['cmd_err'])
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 18)
        result['output'] = str(e)
    finally:
        return result


def upload_arduino(core, tipologia):
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
                result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 19)
                result['output'] = 'OK'
            else:
                raise Exception(response['cmd_err'])
        else:
            raise Exception(DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 38))
    except Exception as e:
        exception("Exception")
        result['result'] = DbManager.select_tb_string_from_lang_value(XmlReader.settings['lingua'], 20)
        result['output'] = str(e)
    finally:
        return result

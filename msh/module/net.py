from os import system
from pexpect import pxssh
from re import sub
import logging


def cmd_ping(ip, pacchetti=5):
    ping_ok = 0
    ping_err = -1
    ping_fail = 1
    file_out = 'pingout.txt'
    result = {'ip': ip,
              'pacchetti_tx': 0,
              'pacchetti_rx': 0,
              'pacchetti_lost': 0,
              'tempo': 0,
              'result': 0,
              'cmd_output': ''
              }
    try:
        system("ping -c %s %s >%s" % (str(pacchetti), ip, file_out))
        f = open("pingout.txt", "r")
        app = f.read()
        f.close()
        system("sudo rm %s" % file_out)
        result['cmd_output'] = app
        app = app.split("\n")
        app = app[len(app) - 3]
        app = app.split(", ")
        result['pacchetti_lost'] = app[2].split(" ")[0]
        result['pacchetti_tx'] = app[0].split(" ")[0]
        result['pacchetti_rx'] = app[1].split(" ")[0]
        result['tempo'] = app[3].split(" ")[1]
        if result['pacchetti_lost'] == '0%':
            result['result'] = ping_ok
        else:
            result['result'] = ping_fail
    except Exception as e:
        result['result'] = ping_err
        result['cmd_output'] = "Error-%s:%s " % ("cmd_ping", e)
    finally:
        return result


def cmd_radioctrl(ip, comando, usr, psw):
    radioctrl_err = -1
    radioctrl_invalid_cred = 2
    radioctrl_no_interface = -2
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
            raise ValueError('SSH session failed on login! -->'+str(ss))

        r = cmd_radiostatus(ip, usr, psw)
        if r['interface'] == '' and r['mac'] == '':
            result['result'] = radioctrl_no_interface
            raise ValueError('Nessuna Interfaccia WiFi Rilevata!')

        result['interface'] = r['interface']
        ss.sendline("ifconfig %s %s" % (result['interface'], result['cmd']))
        ss.prompt()

        r = cmd_radiostatus(ip, usr, psw)
        if r['interface'] == '' and r['mac'] == '':
            result['result'] = radioctrl_no_interface
            raise ValueError('Nessuna Interfaccia WiFi Rilevata!')

        result['mac'] = r['mac']
        result['result'] = r['result']

    except ValueError as v:
        result['cmd_output'] = "Error-%s:%s " % ("cmd_radioctrl", v)

    except Exception as e:
        result['result'] = radioctrl_err
        result['cmd_output'] = "Error-%s:%s " % ("cmd_radioctrl", e)

    finally:
        ss.logout()
        return result


def cmd_radiostatus(ip, usr, psw):
    radiostatus_off = 0
    radiostatus_on = 1
    radioctrl_invalid_cred = 2
    radiostatus_err = -1
    radiostatus_no_interface = -2
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
            raise ValueError('SSH session failed on login! -->'+str(ss))
        ss.sendline("iwconfig")
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
            raise ValueError('Nessuna Interfaccia WiFi Rilevata!')

    except ValueError as v:
        result['cmd_output'] = "Error-%s:%s " % ("cmd_radiostatus", v)

    except Exception as e:
        result['result'] = radiostatus_err
        result['cmd_output'] = "Error-%s:%s " % ("cmd_radiostatus", e)

    finally:
        ss.logout()
        return result


def cmd_pcwin_shutdown(ip, usr, psw):
    pcwin_off_ok = 0
    pcwin_off_err = -1
    pcwin_off_fail = 1
    file_out = 'winpcoffout.txt'
    result = {'ip': ip,
              'result': 0,
              'cmd_output': ''
              }
    try:
        # user%psw
        cred = str(usr) + chr(37) + str(psw)
        system("net rpc shutdown -I %s -U %s >%s" % (ip, cred, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system("sudo rm %s" % file_out)
        result['cmd_output'] = app
        app = sub(r'[\t\n\r]', ' ', app)
        app = app.strip()
        logging.info(app)
        if not app.find('succeeded') == -1:
            result['result'] = pcwin_off_ok
        else:
            result['result'] = pcwin_off_fail
    except Exception as e:
        result['result'] = pcwin_off_err
        result['cmd_output'] = "Error-%s:%s " % ("cmd_pcwin_shutdown", e)

    finally:
        return result


def cmd_wakeonlan(mac, subnet="255.255.255.255"):
    wol_ok = 0
    wol_err = -1
    wol_fail = 1
    file_out = 'wolout.txt'
    result = {'mac': mac,
              'subnet': '',
              'result': 0,
              'cmd_output': ''
              }
    try:
        system("wakeonlan -i %s %s >%s" % (subnet, mac, file_out))
        f = open(file_out, "r")
        app = f.read()
        f.close()
        system("sudo rm %s" % file_out)
        result['cmd_output'] = app
        app = sub(r'[\t\n\r]', ' ', app)
        app = app.strip()
        logging.info(app)
        if not app.find('Sending magic packet') == -1:
            result['result'] = wol_ok
        else:
            result['result'] = wol_fail
    except Exception as e:
        result['result'] = wol_err
        result['cmd_output'] = "Error-%s:%s " % ("cmd_wakeonlan", e)

    finally:
        return result

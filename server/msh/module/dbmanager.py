from sqlite3 import Error, connect
from logging import info
from module import XmlReader
from datetime import datetime


class DbManager:
    db = None
    
    def __init__(self):
        try:
            DbManager.db = connect('db/system.db')
        except Error:
            raise
    
    @staticmethod
    def close_db():
        try:
            DbManager.db.close()
        except Error:
            raise

    @staticmethod
    def select(query):
        try:
            cur = DbManager.db.cursor()
            info("ESEGUO LA QUERY: %s", query)
            cur.execute(str(query))
            result = cur.fetchall()
        except Error:
            DbManager.db.rollback()
            raise
        return result

    @staticmethod
    def insert_or_update(query):
        try:
            cur = DbManager.db.cursor()
            info("ESEGUO LA QUERY: %s", query)
            cur.execute(str(query))
            DbManager.db.commit()
        except Error:
            DbManager.db.rollback()
            raise

    @staticmethod
    def select_tb_net_device(net_mac='', net_code=''):
        query = 'SELECT * ' \
                'FROM TB_NET_DEVICE'
        if net_mac != '':
            query = query + ' WHERE NET_MAC = \'%s\';' % net_mac
        else:
            if net_code != '':
                query = query + ' WHERE NET_CODE = \'%s\';' % net_code
            else:
                query = query + ';'
        net_devices = DbManager.select(query)
        devices = []
        for net_device in net_devices:
            tb_net_device = {
                'net_code': str(net_device[0]),
                'net_desc': str(net_device[1]),
                'net_type': str(net_device[2]),
                'net_status': str(net_device[3]),
                'net_last_update': str(net_device[4]),
                'net_ip': str(net_device[5]),
                'net_mac': str(net_device[6]),
                'net_usr': str(net_device[7]),
                'net_psw': str(net_device[8]),
                'net_mac_info': str(net_device[9])
            }
            devices.append(tb_net_device)
        return devices

    @staticmethod
    def select_tb_net_device_type():
        query = 'SELECT * ' \
                'FROM TB_NET_DEVICE_TYPE;'
        net_devices_type = DbManager.select(query)
        devices_types = []
        for net_device_type in net_devices_type:
            tb_net_device_type = {
                'type_code': str(net_device_type[0]),
                'type_description': str(net_device_type[1])
            }
            devices_types.append(tb_net_device_type)
        return devices_types

    @staticmethod
    def select_tb_net_command_from_type(net_type):
        query = 'SELECT * ' \
                'FROM TB_NET_DIZ_CMD ' \
                'WHERE CMD_NET_TYPE = \'%s\';' % net_type
        net_diz_cmd = DbManager.select(query)
        diz_cmd = []
        for net_cmd in net_diz_cmd:
            tb_net_diz_cmd = {
                'cmd_str': str(net_cmd[0]),
                'cmd_net_type': str(net_cmd[1]),
                'cmd_result': str(net_cmd[2])
            }
            diz_cmd.append(tb_net_diz_cmd)
        return diz_cmd

    @staticmethod
    def select_tb_res_decode_from_type_command_lang_value(device_type, command, lang, value):
        query = 'SELECT * ' \
                'FROM TB_RES_DECODE ' \
                'WHERE RES_DEVICE_TYPE = \'%s\' ' \
                'AND RES_COMMAND = \'%s\' ' \
                'AND RES_LANG = \'%s\' ' \
                'AND RES_VALUE = \'%s\';' % (device_type, command, lang, value)
        res_decodes = DbManager.select(query)
        list_res_decode = []
        for res_decode in res_decodes:
            tb_res_decode = {
                'res_result': str(res_decode[4]),
                'res_state': str(res_decode[5])
            }
            list_res_decode.append(tb_res_decode)
        return list_res_decode[0]

    @staticmethod
    def select_tb_net_device_tb_net_diz_cmd_from_code_and_cmd(net_code, cmd_str):
        query = 'SELECT * ' \
                'FROM TB_NET_DEVICE AS DEV INNER JOIN TB_NET_DIZ_CMD AS DIZ ON DEV.NET_TYPE = DIZ.CMD_NET_TYPE ' \
                'WHERE DEV.NET_CODE = \'%s\' ' \
                'AND DIZ.CMD_STR = \'%s\';' % (net_code, cmd_str)
        net_devices_net_diz_cmd = DbManager.select(query)
        devices_diz_cmd = []
        for net_device in net_devices_net_diz_cmd:
            tb_net_device = {
                'net_code': str(net_device[0]),
                'net_desc': str(net_device[1]),
                'net_type': str(net_device[2]),
                'net_status': str(net_device[3]),
                'net_last_update': str(net_device[4]),
                'net_ip': str(net_device[5]),
                'net_mac': str(net_device[6]),
                'net_usr': str(net_device[7]),
                'net_psw': str(net_device[8]),
                'net_mac_info': str(net_device[9]),
                'cmd_str': str(net_device[10]),
                'cmd_net_type': str(net_device[11]),
                'cmd_result': str(net_device[12])}
            devices_diz_cmd.append(tb_net_device)
        return devices_diz_cmd[0]

    @staticmethod
    def update_tb_net_device(net_mac, net_code=None, net_type=None, net_status=None, net_ip=None, net_user=None, net_psw=None, net_mac_info=None):
        query = 'UPDATE TB_NET_DEVICE SET NET_LASTUPDATE = \'%s\',' % datetime.now().strftime(XmlReader.settings['timestamp'])
        fields = {
            'net_code': 'NET_CODE = \'%s\',' % net_code,
            'net_type': 'NET_TYPE = \'%s\',' % net_type,
            'net_status': 'NET_STATUS = \'%s\',' % net_status,
            'net_ip': 'NET_IP = \'%s\',' % net_ip,
            'net_user': 'NET_USER = \'%s\',' % net_user,
            'net_psw': 'NET_PSW = \'%s\',' % net_psw,
            'net_mac_info': 'NET_MAC_INFO = \'%s\',' % net_mac_info
        }
        device = {
            'net_code': net_code,
            'net_type': net_type,
            'net_status': net_status,
            'net_ip': net_ip,
            'net_user': net_user,
            'net_psw': net_psw,
            'net_mac_info': net_mac_info
        }
        for key, value in device.items():
            if value is not None:
                query = query + fields[key]
        query = query[:-1]
        query = query + ' WHERE NET_MAC = \'%s\';' % net_mac
        DbManager.insert_or_update(query)
        return

    @staticmethod
    def insert_tb_net_device(net_code, net_type, net_status, net_ip, net_user, net_psw, net_mac, net_mac_info):
        query = 'INSERT INTO TB_NET_DEVICE (NET_CODE,NET_TYPE,NET_STATUS,NET_LASTUPDATE,NET_IP,NET_USER,NET_PSW,NET_MAC,NET_MAC_INFO) ' \
                'VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (net_code, net_type, net_status, datetime.now().strftime(XmlReader.settings['timestamp']), net_ip, net_user, net_psw, net_mac, net_mac_info)
        DbManager.insert_or_update(query)

    @staticmethod
    def select_tb_user(username=''):
        query = 'SELECT * ' \
                'FROM TB_USER'
        if username != "":
            query = query + ' WHERE USERNAME = \'%s\';' % username
        else:
            query = query + ';'
        users = DbManager.select(query)
        ret_users = []
        for user in users:
            tb_user = {
                'username': str(user[0]),
                'password': str(user[1]),
                'role': str(user[2]),
            }
            ret_users.append(tb_user)
        return ret_users

    @staticmethod
    def update_tb_user(username, password='', role=''):
        query = 'UPDATE TB_USER SET '
        fields = {
            'password': 'PASSWORD = \'%s\',' % password,
            'role': 'ROLE = \'%s\',' % role,
        }
        device = {
            'password': password,
            'role': role
        }
        for key, value in device.items():
            if value != '':
                query = query + fields[key]
        query = query[:-1]
        query = query + ' WHERE USERNAME = \'%s\';' % username
        DbManager.insert_or_update(query)
        return

    @staticmethod
    def delete_tb_user(username):
        query = 'DELETE FROM TB_USER WHERE USERNAME = \'%s\';' % username
        DbManager.insert_or_update(query)
        return

    @staticmethod
    def insert_tb_user(username, password, role):
        query = 'INSERT INTO TB_USER (USERNAME,PASSWORD,ROLE) ' \
                'VALUES (\'%s\',\'%s\',\'%s\');' % (username, password, role)
        DbManager.insert_or_update(query)

    @staticmethod
    def delete_tb_net_device(mac):
        query = 'DELETE FROM TB_NET_DEVICE WHERE NET_MAC = \'%s\';' % mac
        DbManager.insert_or_update(query)
        return

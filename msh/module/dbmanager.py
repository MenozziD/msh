from sqlite3 import Error, connect
from logging import info


class DbManager:
    db = None
    
    def __init__(self, db_path):
        try:
            DbManager.db = connect(db_path)
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
    def tb_net_device(net_devices):
        devices = []
        for net_device in net_devices:
            tb_net_device = {}
            tb_net_device['net_code'] = str(net_device[0])
            tb_net_device['net_desc'] = str(net_device[1])
            tb_net_device['net_type'] = str(net_device[2])
            tb_net_device['net_status'] = str(net_device[3])
            tb_net_device['net_last_update'] = str(net_device[4])
            tb_net_device['net_ip'] = str(net_device[5])
            tb_net_device['net_mac'] = str(net_device[6])
            tb_net_device['net_usr'] = str(net_device[7])
            tb_net_device['net_psw'] = str(net_device[8])
            tb_net_device['net_mac_info'] = str(net_device[9])
            devices.append(tb_net_device)
        return devices

    @staticmethod
    def tb_net_device_type(net_devices_type):
        devices_types = []
        for net_device_type in net_devices_type:
            tb_net_device_type = {}
            tb_net_device_type['type_code'] = str(net_device_type[0])
            tb_net_device_type['type_description'] = str(net_device_type[1])
            devices_types.append(tb_net_device_type)
        return devices_types

    @staticmethod
    def tb_net_diz_cmd(net_diz_cmd):
        diz_cmd = []
        for net_cmd in net_diz_cmd:
            tb_net_diz_cmd = {}
            tb_net_diz_cmd['cmd_str'] = str(net_cmd[0])
            tb_net_diz_cmd['cmd_net_type'] = str(net_cmd[1])
            tb_net_diz_cmd['cmd_result'] = str(net_cmd[2])
            diz_cmd.append(tb_net_diz_cmd)
        return diz_cmd

    @staticmethod
    def tb_net_device_tb_net_diz_cmd(net_devices_net_diz_cmd):
        devices_diz_cmd = []
        for net_device in net_devices_net_diz_cmd:
            tb_net_device = {}
            tb_net_device['net_code'] = str(net_device[0])
            tb_net_device['net_desc'] = str(net_device[1])
            tb_net_device['net_type'] = str(net_device[2])
            tb_net_device['net_status'] = str(net_device[3])
            tb_net_device['net_last_update'] = str(net_device[4])
            tb_net_device['net_ip'] = str(net_device[5])
            tb_net_device['net_mac'] = str(net_device[6])
            tb_net_device['net_usr'] = str(net_device[7])
            tb_net_device['net_psw'] = str(net_device[8])
            tb_net_device['net_mac_info'] = str(net_device[9])
            tb_net_device['cmd_str'] = str(net_device[10])
            tb_net_device['cmd_net_type'] = str(net_device[11])
            tb_net_device['cmd_result'] = str(net_device[12])
            devices_diz_cmd.append(tb_net_device)
        return devices_diz_cmd

    @staticmethod
    def tb_res_decode(res_decodes):
        list_res_decode = []
        for res_decode in res_decodes:
            tb_res_decode = {}
            tb_res_decode['res_result'] = str(res_decode[4])
            tb_res_decode['res_state'] = str(res_decode[5])
            list_res_decode.append(tb_res_decode)
        return list_res_decode

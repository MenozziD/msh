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

    # DbManager.select(XmlReader.settings['query']['select_tb_net_device'])
    # DbManager.select(XmlReader.settings['query']['select_one_tb_net_device'] % net_code)
    # DbManager.select(XmlReader.settings['query']['select_last_tb_net_com'])
    # DbManager.select(XmlReader.settings['query']['select_tb_net_diz_cmd'] % (net_code, cmd_str))
    # DbManager.select(XmlReader.settings['query']['select_one_tb_res_decode'] % (res_device_type, res_device_subtype, res_command, res_lang, res_value))
    # DbManager.insert_or_update(XmlReader.settings['query']['insert_tb_net_device'] % (net_code, net_type, net_status, net_ip, net_mac, net_mac_info))
    # DbManager.insert_or_update(XmlReader.settings['query']['update_tb_net_device'] % (net_code, net_type, net_status, net_ip, net_mac_info, net_mac))
    # DbManager.insert_or_update(XmlReader.settings['query']['update_state_from_ip_tb_net_device'] % (net_status, net_ip))

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import logging
from module.utility import XmlReader


class DbManager:
    db = None
    error_db = XmlReader.settings['string_failure']['error_db']
    error = XmlReader.settings['string_failure']['error']
    
    def __init__(self, db_path):
        try:
            DbManager.db = lite.connect(db_path)
        except lite.Error as e:
            logging.error(XmlReader.settings['string_failure']['open_db'] + e)
        return
    
    @staticmethod
    def close_db():
        try:
            if DbManager.db:
                DbManager.db.close()
        except lite.Error as e:
            logging.error(XmlReader.settings['string_failure']['close_db'] + e)

    @staticmethod
    def select_tb_net_device():
        r = ''
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_tb_net_device'])
                r = cur.fetchall()
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            return r

    @staticmethod
    def select_one_tb_net_device(net_code):
        result = ''
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_one_tb_net_device'] % net_code)
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        result = row
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            return result

    @staticmethod
    def insert_tb_net_device(net_code, net_desc, net_name, net_type, net_status, net_ip, net_mac, net_mac_info):
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['insert_tb_net_device'] % (net_code, net_desc, net_name, net_type, net_status, net_ip, net_mac, net_mac_info))
                DbManager.db.commit()
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))

    @staticmethod
    def select_last_tb_net_com():
        result = ''
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_last_tb_net_com'])
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        result = row
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            return result

    @staticmethod
    def select_tb_net_diz_cmd(net_code, cmd_str):
        result = ""
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_tb_net_diz_cmd'] % (net_code, cmd_str))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        result = row
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.error_db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            return result

    @staticmethod
    def update_state_from_ip_tb_net_device(net_ip, net_status):
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_tb_net_diz_cmd'] % (net_status, net_ip))
                DbManager.db.commit()
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            pass

    @staticmethod
    def select_one_tb_res_decode(res_device_type, res_device_subtype, res_command, res_lang, res_value):
        result = ""
        try:
            if DbManager.db:
                cur = DbManager.db.cursor()
                cur.execute(XmlReader.settings['query']['select_one_tb_res_decode'] % (res_device_type, res_device_subtype, res_command, res_lang, res_value))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        result = row
            else:
                logging.error(DbManager.error_db)
        except lite.Error as e:
            DbManager.db.rollback()
            logging.error(DbManager.error + str(e))
        finally:
            return result

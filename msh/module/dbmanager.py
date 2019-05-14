#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
from module import utility


def open_db(db_path):
    db = None
    try:
        db = lite.connect(db_path)
    except lite.Error as e:
        print(utility.XmlReader.settings['string_failure']['openDB'], e)
    finally:
        return db


def close_db(db):
    try:
        if db:
            db.close()
    except lite.Error as e:
        print(utility.XmlReader.settings['string_failure']['closeDB'], e)
    finally:
        return db


'''
------------------------------------------------------------------------------------------------------------------------
                                                        NET
------------------------------------------------------------------------------------------------------------------------
'''


def select_tb_net_device(db):
    r = ''
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_tb_net_device'])
            r = cur.fetchall()
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return r


def select_one_tb_net_device(db, net_code):
    result = ''
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_one_tb_net_device'] % net_code)
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result


def insert_tb_net_device(db, net_code, net_desc, net_name, net_type, net_status, net_ip, net_mac, net_mac_info):
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['insert_tb_net_device'] % (net_code, net_desc, net_name, net_type, net_status, net_ip, net_mac, net_mac_info))
            db.commit()
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)


def select_last_tb_net_com(db):
    result = ''
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_last_tb_net_com'])
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result


def select_tb_net_diz_cmd(db, net_code, cmd_str):
    result = ""
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_tb_net_diz_cmd'] % (net_code, cmd_str))
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result


def update_state_from_ip_tb_net_device(db, net_ip, net_status):
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_tb_net_diz_cmd'] % (net_status, net_ip))
            db.commit()
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        pass


def select_one_tb_res_decode(db, res_device_type, res_device_subtype, res_command, res_lang, res_value):
    result = ""
    try:
        if db:
            cur = db.cursor()
            cur.execute(utility.XmlReader.settings['query']['select_one_tb_res_decode'] % (res_device_type, res_device_subtype, res_command, res_lang, res_value))
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print(utility.XmlReader.settings['string_failure']['errorDB'])
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result

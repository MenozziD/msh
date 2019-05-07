#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite


def open_db(db_path):
    db = None
    try:
        db = lite.connect(db_path)
    except lite.Error as e:
        print("DB OPEN Error:", e)
    finally:
        return db


def print_sql_version(db):
    try:
        if db:
            cur = db.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            print("SQLite version: %s" % data)
        else:
            print("DB not init!")
    except lite.Error as e:
        print("Error:", e)


def close_db(db):
    try:
        if db:
            db.close()
    except lite.Error as e:
        print("DB CLOSE Error:", e)
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
            s = "SELECT net_code,net_desc,net_status,NET_LASTUPDATE,net_ip,net_mac "
            s = s + "FROM TB_NET_DEVICE;"
            cur.execute(s)
            r = cur.fetchall()

        else:
            print("DB not init!")
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
            s = "SELECT net_code,net_desc,net_status,NET_LASTUPDATE,net_ip,net_mac,NET_CREDENTIAL "
            s = s + "FROM TB_NET_DEVICE "
            s = s + "WHERE net_code like '%s';" % net_code
            cur.execute(s)
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print("DB not init!")
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result


def insert_tb_net_device(db, net_code, net_desc, net_name, net_type, net_status, net_ip, net_mac, net_mac_info):
    try:
        if db:
            cur = db.cursor()
            s = "INSERT INTO TB_NET_DEVICE (net_code,net_desc,net_name,net_type,net_status,net_ip,net_mac,net_mac_info) "
            s = s + "VALUES ('" + net_code + "','" + net_desc + "','" + net_name + "', "
            s = s + "'" + net_type + "','" + net_status + "','" + net_ip + "','" + net_mac + "','" + net_mac_info + "'); "
            cur.execute(s)
            db.commit()
        else:
            print("DB not init!")
    except lite.Error as e:
        db.rollback()
        print("Error:", e)


def select_last_tb_net_com(db):
    result = ''
    try:
        if db:
            cur = db.cursor()
            s = "SELECT REQ_ID,REQ_NODE,REQ_CMD,REQ_RESPONSE,REQ_RESULT,REQ_DATETIME "
            s = s + "FROM TB_NET_COM ORDER BY REQ_ID DESC LIMIT 1;"
            cur.execute(s)
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print("DB not init!")
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
            s = "SELECT TB_NET_DEVICE.net_code,TB_NET_DEVICE.net_type, TB_NET_DEVICE.net_ip, TB_NET_DEVICE.net_mac, "
            s = s + "TB_NET_DIZ_CMD.cmd_str, TB_NET_DIZ_CMD.CMD_RESULT, TB_NET_DEVICE.NET_USER, TB_NET_DEVICE.NET_PSW "
            s = s + "FROM TB_NET_DEVICE "
            s = s + "INNER JOIN TB_NET_DIZ_CMD ON TB_NET_DEVICE.net_type = TB_NET_DIZ_CMD.CMD_net_type "
            s = s + "WHERE TB_NET_DEVICE.net_code LIKE '%s' AND TB_NET_DIZ_CMD.cmd_str LIKE '%s'" % (net_code, cmd_str)
            cur.execute(s)
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print("DB not init!")
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result


def update_state_from_ip_tb_net_device(db, net_ip, net_status):
    try:
        if db:
            s = "UPDATE TB_NET_DEVICE "
            s = s + "SET net_status = '%s' " % net_status
            s = s + "WHERE net_ip like '%s';" % net_ip
            cur = db.cursor()
            cur.execute(s)
            db.commit()
        else:
            print("DB not init!")

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
            s = "SELECT RES_RESULT, RES_STATE "
            s = s + "FROM TB_RES_DECODE "
            s = s + "WHERE res_device_type like '%s' and res_device_subtype like '%s' " % (
                res_device_type, res_device_subtype)
            s = s + "and res_command like '%s' " % res_command
            s = s + "and res_lang like '%s' and res_value == %s ;" % (res_lang, res_value)
            cur.execute(s)
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    result = row
        else:
            print("DB not init!")
    except lite.Error as e:
        db.rollback()
        print("Error:", e)
    finally:
        return result

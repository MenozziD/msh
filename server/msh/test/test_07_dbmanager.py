from unittest import TestCase
from test import read_xml
from module import DbManager
from pytest import raises


class TestDbManager(TestCase):

    def test_select_not_correct(self):
        read_xml()
        DbManager()
        with raises(Exception):
            DbManager.select("SELECT * FROMM")
        DbManager.close_db()

    def test_update_not_correct(self):
        read_xml()
        DbManager()
        with raises(Exception):
            DbManager.insert_or_update("UPPDATE TABELLA")
        DbManager.close_db()

#!/usr/bin/env python
# encoding: utf-8

from conftests import *
from rurouni.exceptions import *
from rurouni import Database

def test_simple_database_init():
    db = Database('sqlite:///:memory:')
    db.destroy()

def test_multiple_database(db):
    db1 = Database('sqlite:////tmp/tmp_db1.sqlite')
    db2 = Database('sqlite:////tmp/tmp_db2.sqlite')

    assert db1._engine.url.database == '/tmp/tmp_db1.sqlite'
    assert db2._engine.url.database == '/tmp/tmp_db2.sqlite'

    db1.destroy()
    db2.destroy()

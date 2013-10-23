#!/usr/bin/env python
# encoding: utf-8

from conftests import *
from rurouni.exceptions import *
from rurouni import Database

def test_simple_database_init():
    db = Database('sqlite:///:memory:')
    db.destroy()

def test_duplicated_database(db):
    with pytest.raises(DuplicatedConnection):
        db2 = Database('sqlite:///:memory:')
    assert 'db2' not in locals()
    db.destroy()

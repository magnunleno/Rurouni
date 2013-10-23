#!/usr/bin/env python
# encoding: utf-8

from conftests import *

from rurouni.exceptions import *
from rurouni.types import *
from rurouni import Database, Column, Table

def test_table_simple_init(db):
    class Client(Table):
        first_name = Column(String)
        last_name = Column(String)

    assert Client.__tablename__ == "client"
    assert db._hasSQLATable("client")
    db.destroy()

def test_table_custom_name_init(db):
    class Client(Table):
        __tablename__ = "tb001_client"
        first_name = Column(String)
        last_name = Column(String)

    assert Client.__tablename__ == "tb001_client"
    assert db._hasSQLATable("tb001_client")
    db.destroy()

def test_table_auto_id_column(db):
    class Client(Table):
        first_name = Column(String)
        last_name = Column(String)

    # ID Properties
    cols = Client.__sqlacolumns__
    assert 'id' in cols
    assert isinstance(cols['id'].type, Integer)
    assert cols['id'].primary_key
    assert cols['id'].autoincrement
    db.destroy()

def test_table_columns_names_and_types(db):
    class Client(Table):
        id = Column(Integer, primary_key=True)
        name = Column(String)
        birth_date = Column(Date)

    cols = Client.__sqlacolumns__

    # Column Names
    assert 'id' in cols
    assert 'name' in cols
    assert 'birth_date' in cols

    # Column Types
    assert isinstance(cols['id'].type, Integer)
    assert isinstance(cols['name'].type, String)
    assert isinstance(cols['birth_date'].type, Date)

    # ID Properties
    assert cols['id'].primary_key
    assert cols['id'].autoincrement
    db.destroy()

def test_table_logging(ldb):
    class Client(Table):
        name = Column(String)
        birth_date = Column(Date)

    logs = ldb.getLog()
    out = [
            'PRAGMA table_info("client")', 
            'CREATE TABLE client (',
            'birth_date DATE,', 
            'name VARCHAR,', 
            'id INTEGER NOT NULL,',
            'PRIMARY KEY (id)', 
            ')', 
            'COMMIT'
            ]
    assert logs == out
    ldb.destroy()

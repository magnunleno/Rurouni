#!/usr/bin/env python
# encoding: utf-8

from conftests import *

from rurouni.exceptions import *
from rurouni.types import *
from rurouni import Database, Column, Table

def test_mult_db():
    db1 = Database('sqlite:///:memory:')
    db2 = Database('sqlite:///:memory:')
    class Client(Table):
        __db__ = db1
        first_name = Column(String)

    assert db1.getTableNames() == ['client']
    assert db2.getTableNames() == []

    class ForeignClient(Table):
        __db__ = db2
        first_name = Column(String)

    assert db1.getTableNames() == ['client']
    assert db2.getTableNames() == ['foreignclient']

    class Product(Table):
        __db__ = db1
        name = Column(String)

    assert db1.getTableNames() == ['product', 'client']
    assert db2.getTableNames() == ['foreignclient']

    db1.destroy()
    db2.destroy()

def test_default_db():
    db1 = Database('sqlite:///:memory:')
    db2 = Database('sqlite:///:memory:')
    Table.__db__ = db1

    class Client(Table):
        first_name = Column(String)

    assert db1.getTableNames() == ['client']
    assert db2.getTableNames() == []

    class Product(Table):
        name = Column(String)

    assert db1.getTableNames() == ['product', 'client']
    assert db2.getTableNames() == []

    class ForeignClient(Table):
        __db__ = db2
        first_name = Column(String)

    assert db1.getTableNames() == ['product', 'client']
    assert db2.getTableNames() == ['foreignclient']

    db1.destroy()
    db2.destroy()

def test_table_simple_init(db):
    class Client(Table):
        __db__ = db
        first_name = Column(String)
        last_name = Column(String)

    assert Client.__tablename__ == "client"
    assert db._hasSQLATable("client")
    db.destroy()

def test_table_custom_name_init(db):
    class Client(Table):
        __db__ = db
        __tablename__ = "tb001_client"
        first_name = Column(String)
        last_name = Column(String)

    assert Client.__tablename__ == "tb001_client"
    assert db._hasSQLATable("tb001_client")
    db.destroy()

def test_table_auto_id_column(db):
    class Client(Table):
        __db__ = db
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
        __db__ = db
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
        __db__ = ldb.db
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

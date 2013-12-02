#!/usr/bin/env python
# encoding: utf-8

from conftests import *
from rurouni.types import *
from rurouni import Database,Table,Column

def test_simple_database_init():
    db = Database('sqlite:///:memory:')
    db.destroy()

def test_multiple_database():
    db1 = Database('sqlite:////tmp/tmp_db1.sqlite')
    db2 = Database('sqlite:////tmp/tmp_db2.sqlite')

    assert db1._engine.url.database == '/tmp/tmp_db1.sqlite'
    assert db2._engine.url.database == '/tmp/tmp_db2.sqlite'

    db1.destroy()
    db2.destroy()

def test_table_listing(db):
    Table.__db__ = db
    assert db.getTableNames() == []
    assert db.all() == []
    assert len(db) == 0

    class Client(Table):
        name = Column(String)
    assert db.getTableNames() == ['client']
    assert db.all() == [Client]
    assert len(db) == 1

    class Product(Table):
        name = Column(String)
    assert db.getTableNames() == ['product', 'client']
    assert db.all() == [Product, Client]
    assert len(db) == 2

    class User(Table):
        name = Column(String)
    assert db.getTableNames() == ['product', 'client', 'user']
    assert db.all() == [Product, Client, User]
    assert len(db) == 3

    db.destroy()

def test_table_searching(db):
    Table.__db__ = db

    assert db.hasTable('client') == False
    assert db.getTable('client') == None
    assert db['client'] == None

    class Client(Table):
        name = Column(String)

    assert db.hasTable('client') == True
    assert db.getTable('client') == Client
    assert db['client'] == Client

    class Product(Table):
        name = Column(String)
    assert db.hasTable('client') == True
    assert db.getTable('client') == Client
    assert db['client'] == Client

    assert db.hasTable('product') == True
    assert db.getTable('product') == Product
    assert db['product'] == Product

    assert db.hasTable('user') == False
    assert db.getTable('user') == None
    assert db['user'] == None

    db.destroy()

def test_database_iteration(db):
    Table.__db__ = db
    assert [table for table in db] == []

    class Client(Table):
        name = Column(String)
    assert [table for table in db] == [Client]

    class Product(Table):
        name = Column(String)
    assert [table for table in db] == [Product, Client]

    class User(Table):
        name = Column(String)
    assert [table for table in db] == [Product, Client, User]

    db.destroy()

def test_sqla_table_listing(db):
    Table.__db__ = db
    assert db._hasSQLATable('client') == False
    with pytest.raises(KeyError):
        db._getSQLATable('client')
    assert db._getSQLATableNames() == []

    class Client(Table):
        name = Column(String)
    assert db._hasSQLATable('client') == True
    assert db._getSQLATable('client') == Client.__sqlatable__
    assert db._getSQLATableNames() == ['client']

    class Product(Table):
        name = Column(String)
    assert db._hasSQLATable('client') == True
    assert db._getSQLATable('client') == Client.__sqlatable__
    assert db._getSQLATableNames() == ['client', 'product']

    assert db._hasSQLATable('product') == True
    assert db._getSQLATable('product') == Product.__sqlatable__
    assert db._getSQLATableNames() == ['client', 'product']

    assert db._hasSQLATable('user') == False
    with pytest.raises(KeyError):
        db._getSQLATable('user')

    db.destroy()

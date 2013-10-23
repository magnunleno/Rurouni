#!/usr/bin/env python
# encoding: utf-8

import pytest
from conftests import *

from rurouni.exceptions import *
from rurouni.types import *
from rurouni import Database, Column, Table

def test_column_appending(ldb):
    '''
    Checks column appending. To simulate this behaviour just adds two different
    classes pointing to the same table.
    '''
    # First declaration
    class Client(Table):
        pass
    ldb.flush()

    # Second declaration
    class NewClient(Table):
        __tablename__ = 'client'
        name = Column(String)

    # Check logs
    logs = ldb.getLog()
    assert logs[0] == 'PRAGMA table_info("client")'
    assert logs[1] == 'ALTER TABLE client ADD name VARCHAR'
    assert logs[2] == 'COMMIT'
    ldb.destroy()

def test_column_removal(ldb):
    '''
    Checks column removal. To simulate this behaviour just adds two different
    classes pointing to the same table.
    For this is needed to set the db.autoremove_columns flag as True.
    '''
    ldb.db.autoremove_columns = True

    # First declaration
    class Client(Table):
        firstname = Column(String)
        lastname = Column(String)
    ldb.flush()

    # Second declaration
    class NewClient(Table):
        __tablename__ = 'client'
        firstname = Column(String)

    # Check logs
    logs = ldb.getLog()
    assert logs[0] == 'PRAGMA table_info("client")'
    assert logs[1] == 'ALTER TABLE client RENAME TO migration_tmp'
    assert logs[2] == 'COMMIT'
    assert logs[3] == 'CREATE TABLE client ('
    assert logs[4] == 'id INTEGER NOT NULL,'
    assert logs[5] == 'firstname VARCHAR,'
    assert logs[6] == 'PRIMARY KEY (id)'
    assert logs[7] == ')'
    assert logs[8] == 'COMMIT'
    assert logs[9] == 'INSERT INTO client SELECT id ,firstname from migration_tmp'
    assert logs[10] == 'COMMIT'
    assert logs[11] == 'DROP TABLE migration_tmp'
    assert logs[12] == 'COMMIT'
    ldb.destroy()

def test_table_removal(tmp_ldb):
    '''
    Test table removal. For this feature the db.autoClean() must be called at
    the end of all table definition.
    Also, is nedded to be a persistent database.
    '''
    # Define two tables
    class Client(Table):
        pass
    class Profession(Table):
        pass

    # Reopen db and define only one table
    tmp_ldb.reopen()
    class Client(Table):
        pass

    tmp_ldb.flush() # Flush output
    tmp_ldb.db.autoClean() # Autoclean tables

    # Table profession must be dropped
    logs = tmp_ldb.getLog()
    assert logs[0] == 'DROP TABLE profession'
    assert logs[1] == 'COMMIT'
    # Remove file
    tmp_ldb.whipeout()

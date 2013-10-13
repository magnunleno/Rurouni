#!/usr/bin/env python
# encoding: utf-8

import pytest
from rurouni.exceptions import *

def test_simple_database_init():
    from rurouni.database import Database
    db = Database('sqlite:///:memory:')
    db.destroy()

def test_duplicated_database():
    from rurouni.database import Database
    db1 = Database('sqlite:///:memory:')
    with pytest.raises(DuplicatedConnection):
        db2 = Database('sqlite:///:memory:')
    db1.destroy()

#!/usr/bin/env python
# encoding: utf-8

from conftests import *
from rurouni.exceptions import *
from rurouni.types import *
from rurouni import Database, Column, Table

def test_insert_errors(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    with pytest.raises(UnknownField):
        id = Client.insert(name="John", last_name="Doe")
    assert 'id' not in locals()

    db.destroy()

def test_insert(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)
    
    name1 = "John"
    birthdate1 = randomDate()
    name2 = "Jack"
    birthdate2 = randomDate()
    name3 = "Bob"
    birthdate3 = randomDate()
    c1 = Client.insert(name=name1, birthdate=birthdate1)
    c2 = Client.insert(name=name2, birthdate=birthdate2)
    c3 = Client.insert(name=name3, birthdate=birthdate3)

    assert c1._id == 1
    assert c1.name == name1
    assert c1.birthdate == birthdate1

    assert c2._id == 2
    assert c2.name == name2
    assert c2.birthdate == birthdate2

    assert c3._id == 3
    assert c3.name == name3
    assert c3.birthdate == birthdate3

    db.destroy()

def test_insert_many_errors(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)
    
    with pytest.raises(InvalidData):
        Client.insert_many() == []
    with pytest.raises(InvalidData):
        Client.insert_many(None, None)
    with pytest.raises(InvalidData):
        Client.insert_many({})
    with pytest.raises(UnknownField):
        Client.insert_many({'n':'err'})

    data = [
            {'name':'John', 'birthdate':randomDate()},
            {'name':'Jack', 'birthdate':randomDate()},
            {'name':'Bob', 'birthdate':randomDate()},
            ]
    Client.insert_many(*data)

    for i, data in enumerate(data, 1):
        c = Client(i)
        assert c.name == data['name']
        assert c.birthdate == data['birthdate']
    db.destroy()

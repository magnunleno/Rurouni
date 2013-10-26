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

def test_hasId(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    assert not Client.has(1)
    assert not (1 in Client)
    c = Client.insert(name='John', birthdate=randomDate())
    assert c.id == 1
    assert Client.has(1)
    assert 1 in Client
    db.destroy()

def test_delete(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    data = [
            {'name':'John', 'birthdate':randomDate()},
            {'name':'Jack', 'birthdate':randomDate()},
            {'name':'Bob', 'birthdate':randomDate()},
            ]
    Client.insert_many(*data)

    assert Client.has(1) == True
    assert Client.has(2) == True
    assert Client.has(3) == True

    Client.delete(2)

    assert Client.has(1) == True
    assert Client.has(2) == False
    assert Client.has(3) == True
    db.destroy()

def test_iter(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    data = [
            {'name':'John', 'birthdate':randomDate()},
            {'name':'Jack', 'birthdate':randomDate()},
            {'name':'Bob', 'birthdate':randomDate()},
            ]
    Client.insert_many(*data)

    # Iterate using Client.all()
    count = 0
    for (n, c) in enumerate(Client.all()):
        vals = data[n]
        assert c.id == n + 1
        assert c.name == vals['name']
        assert c.birthdate == vals['birthdate']
        count += 1
    assert count == 3

    # Iterate using Client.__iter__
    count = 0
    for (n, c) in enumerate(Client):
        vals = data[n]
        assert c.id == n + 1
        assert c.name == vals['name']
        assert c.birthdate == vals['birthdate']
        count += 1
    assert count == 3
    db.destroy()

def test_count(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    assert Client.count() == 0
    Client.insert(name='John', birthdate=randomDate())
    assert Client.count() == 1
    Client.insert(name='Jack', birthdate=randomDate())
    assert Client.count() == 2
    Client.insert(name='Bob', birthdate=randomDate())
    assert Client.count() == 3
    db.destroy()

def test_empty(db):
    class Client(Table):
        name = Column(String)
        birthdate = Column(Date)

    assert Client.isEmpty() == True
    Client.insert(name='John', birthdate=randomDate())
    assert Client.isEmpty() == False
    db.destroy()

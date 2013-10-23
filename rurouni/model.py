#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2012 - Magnun Leno
#
# This file is part of Rurouni.
#
# Rurouni is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Rurouni is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Rurouni If not, see http://www.gnu.org/licenses/.

from .exceptions import *
from .metamodel import MetaTable
from sqlalchemy.sql import select as _select
from sqlalchemy.sql import insert as _insert

class Table(object):
    __metaclass__ = MetaTable
    def __init__(self, id):
        self._id = id

    @classmethod
    def getById(kls, id):
        # TODO: review if this method is needed
        s = _select([kls.id._sqla_column])
        conn = kls.__db__._engine.connect()
        result = conn.execute(s)
        if result.fetchone():
            conn.close()
            return kls(id)
        else:
            conn.close()
            raise UnknownInstanceID("%i"%id)

    @classmethod
    def insert(kls, **kwargs):
        diff = set(kwargs.keys()) - set(kls.__columns__.keys())
        if diff:
            raise UnknownField(', '.join(diff))
        ins = kls.__sqlatable__.insert().values().values(**kwargs)
        conn = kls.__db__._engine.connect()
        result = conn.execute(ins)
        if result.rowcount == 1:
            id = result.inserted_primary_key[0]
            conn.close()
            return kls(id)
        conn.close()

    @classmethod
    def insert_many(kls, *data):
        if not data or len(data) == 0:
            raise InvalidData("Empty data")

        valid_keys = set(kls.__columns__.keys())
        for d in data:
            if not d:
                raise InvalidData(`d`)
            try:
                diff = set(d.keys()) - valid_keys
            except AttributeError:
                raise InvalidData(`d`)

            if diff:
                raise UnknownField(', '.join(diff))

        table = kls.__sqlatable__
        conn = kls.__db__._engine.connect()
        trans = conn.begin()

        try:
            result = conn.execute(table.insert(), data)
            trans.commit()
        except:
            trans.rollback()
            conn.close()
            raise
        conn.close()
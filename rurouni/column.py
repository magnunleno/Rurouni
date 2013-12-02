#!/usr/bin/env python
# encoding: utf-8
#
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

from sqlalchemy.schema import Column as _Column
from sqlalchemy.types import AbstractType as _AbstractType
from sqlalchemy.sql import select as _select
from .exceptions import *

class Column(object):
    def __init__(self, type, *args, **kwargs):
        if not isinstance(type(), _AbstractType):
            raise InvalidColumnType("Type should be from rurouni.types")
        self._type = type
        self._args = args
        self._kwargs = kwargs
        self._sqla_column = None

    def _build_column(self, name):
        self._sqla_column = _Column(name, self._type, *self._args, **self._kwargs)
        return self._sqla_column

    def __get__(self, obj, type=None):
        # TODO: Implement cache
        if self._sqla_column.name == 'id':
            return obj._id

        if not obj:
            return self
        sqla_table = obj.__sqlatable__
        db = obj.__db__
        exp = sqla_table.columns.id == obj._id

        conn = db._engine.connect()
        sel = _select([self._sqla_column]).where(exp)
        result = conn.execute(sel)
        result = result.fetchone()
        conn.close()

        return result[0]

    def __set__(self, obj, value):
        sqla_table = obj.__sqlatable__
        db = obj.__db__
        values = {self._sqla_column.name:value}
        exp = sqla_table.columns.id == obj._id

        conn = db._engine.connect()
        update = sqla_table.update([sqla_table]).where(exp)
        update.values(**values)

        result = conn.execute(sel)
        result = result.fetchone()
        conn.close()

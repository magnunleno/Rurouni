#!/usr/bin/env python
# encoding: utf-8

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
        if self._sqla_column.name == 'id':
            return obj._id

        if not obj:
            return self
        table = obj.__sqlatable__
        db = obj.__db__
        exp = table.columns.id == obj._id

        conn = db._engine.connect()
        sel = _select([self._sqla_column]).where(exp)
        result = conn.execute(sel)
        result = result.fetchone()
        conn.close()

        return result[0]

    def __set__(self, obj, value):
        table = obj.__sqlatable__
        db = obj.__db__
        values = {self._sqla_column.name:value}
        exp = table.columns.id == obj._id

        conn = db._engine.connect()
        update = table.update([table]).where(exp)
        update.values(**values)

        result = conn.execute(sel)
        result = result.fetchone()
        conn.close()

#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy.schema import Column as _Column
from sqlalchemy.types import AbstractType as _AbstractType
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
        if not obj:
            return self
        print 'get',obj, self._type, self._sqla_column

    def __set__(self, obj, value):
        print 'set', obj, value

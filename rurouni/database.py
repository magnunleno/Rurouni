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

from sqlalchemy.schema import MetaData as _MetaData
from sqlalchemy import create_engine as _create_engine
from migrate.versioning.util import construct_engine as _construct_engine
from .exceptions import *

class Database(object):
    def __init__(self, *args, **kwargs):
        engine = _create_engine(*args, **kwargs)
        self._engine = _construct_engine(engine)
        self._metadata = _MetaData()
        self._metadata.bind = engine
        self._metadata.reflect(engine)

        self._tables = {}

        self.autoremove_columns = False
        self.autoremove_tables = False

    def destroy(self):
        e = self._engine
        (self._engine, self._metadata) = (None, None)
        self._tables = {}
        del e

    def _hasSQLATable(self, tablename):
        return self._engine.has_table(tablename)

    def _getSQLATable(self, tablename):
        return self._metadata.tables[tablename]

    def _getSQLATableNames(self):
        return self._engine.table_names()

    def hasTable(self, tablename):
        return tablename in self._tables

    def getTable(self, tablename):
        return self._tables.get(tablename, None)

    def getTableNames(self):
        return self._tables.keys()

    def all(self):
        return self._tables.values()

    def autoClean(self):
        sqlaTables = set(self._metadata.tables.keys())
        tables = set(self._tables.keys())
        for tablename in sqlaTables - tables:
            table = self._metadata.tables[tablename]
            table.drop()

    def __iter__(self):
        for table in self._tables.values():
            yield table

    def __getitem__(self, key):
        if key not in self._tables:
            return None

        return self._tables[key]
    
    def __len__(self):
        return len(self._tables)

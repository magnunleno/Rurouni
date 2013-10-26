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

from .column import Column
from .database import getDatabase

from sqlalchemy.schema import Table as _Table
from sqlalchemy.types import Integer as _Integer

class MetaTable(type):
    def __init__(table, name, bases, attr):
        # Avoid initiating the Table Class
        if bases[0] == object:
            return

        if ('__tablename__' not in attr) or (not table.__tablename__):
            # If no tablename is specified
            tablename = name.lower()
            table.__tablename__ = tablename
        else:
            tablename = attr['__tablename__']

        # Filter the Columns
        columns = {n:c for n, c in attr.items() if isinstance(c, Column)}

        # Force the id column
        if 'id' not in columns:
            columns['id'] = Column(_Integer, primary_key=True)
            setattr(table, 'id', columns['id'])

        db = getDatabase()
        if not db._hasSQLATable(tablename):
            (sqla_table, sqla_columns) = MetaTable.createTable(db, table, columns)
        else:
            (sqla_table, sqla_columns) = MetaTable.alterTable(db, table, columns)

        # "Register" the table in the database
        db._tables[tablename] = table

        # Inject some informations in the table
        table.__db__ = db
        table.__sqlatable__ = sqla_table
        table.__sqlacolumns__ = sqla_columns
        table.__columns__ = columns

        # Inject some informations in the columns
        for column in columns.values():
            column._table = table

    @staticmethod
    def createTable(db, table, columns):
        sqla_columns = {name:data._build_column(name) for name,data in columns.items()}
        sqla_table = _Table(table.__tablename__, db._metadata, *sqla_columns.values())
        sqla_table.create()
        return (sqla_table, sqla_columns)

    @staticmethod
    def alterTable(db, table, columns):
        sqla_table = db._getSQLATable(table.__tablename__)
        # new_columns = rurouni columns
        new_columns = {name:data._build_column(name) for name,data in columns.items()}
        # old_columns = sqla_columns
        old_columns = {column.name:column for column in sqla_table.columns}

        # Remove unused columns
        if db.autoremove_columns:
            for name in set(old_columns.keys()) - set(new_columns.keys()):
                col = old_columns[name]
                col.drop()

        # Add new columns
        for name in set(new_columns.keys()) - set(old_columns.keys()):
            col = new_columns[name]
            col.create(sqla_table, populate_default=True)

        return (sqla_table, old_columns)

    def __contains__(kls, id):
        return kls.has(id)

    def __iter__(kls):
        return kls.all()

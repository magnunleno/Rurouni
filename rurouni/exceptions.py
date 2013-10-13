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

class RurouniException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class DuplicatedConnection(RurouniException):
    pass

class InvalidColumnType(RurouniException):
    pass

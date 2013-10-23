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

'''
Tomorrow will take us away
far from home.
No one will ever know our names,
but the bard's songs will remain.
Tomorrow will take it away.
The fear of today,
it will be gone,
due to our magic songs
              - The Bard's Song (Blind Guardian)
'''

__version__ = "0.1.0"
__author__ = "Magnun Leno"

from .column import Column
from .model import Table
from .database import getDatabase, Database
from . import types

# content of conftest.py

import pytest
from rurouni import Database
from StringIO import StringIO
from datetime import date
from random import random
from math import ceil
from os import remove as rm
import logging

class LoggedDB(object):
    def __init__(self, db_str):
        self.db = Database(db_str)
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logging.basicConfig(format="%(message)s")
        self.logger = logging.getLogger('sqlalchemy.engine.base.Engine')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        self.db_str = db_str

    def flush(self):
        self.handler.flush()
        self.stream.getvalue()
        self.stream.truncate(0)

    def destroy(self):
        self.db.destroy()
        self.handler.close()

    def destroy(self):
        self.db.destroy()
        self.handler.close()

    def whipeout(self):
        fdb = self.db._engine.url.database
        self.destroy()
        if fdb != ':memory:':
            rm(fdb)

    def reopen(self):
        self.destroy()

        self.db = Database(self.db_str)
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logging.basicConfig(format="%(message)s")
        self.logger = logging.getLogger('sqlalchemy.engine.base.Engine')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def getLog(self):
        self.handler.flush()
        logs = self.stream.getvalue().split('\n')
        cleaned_logs = []
        for log_line in logs:
            log_line = log_line.strip()
            if log_line == "()":
                continue
            if log_line:
                cleaned_logs.append(log_line)
        return cleaned_logs

def randomDate():
    today = date.today()
    day = int(ceil(random()*29))
    month = int(ceil(random()*12))
    return today.replace(day=day,month=month)

@pytest.fixture
def db():
    return Database('sqlite:///:memory:')

@pytest.fixture
def ldb():
    return LoggedDB('sqlite:///:memory:')

@pytest.fixture
def tmp_ldb():
    return LoggedDB('sqlite:////tmp/rurouni.sqlite')

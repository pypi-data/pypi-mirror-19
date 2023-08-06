import sqlite3

import numpy


class Sqlite:
    def __init__(self, uri):
        self.engine = sqlite3.connect(uri)

    def __del__(self):
        if self.engine:
            self.engine.commit()
            self.engine.close()
            self.engine = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def exec(self, script, *params):
        print(script, params)
        return self.engine.execute(script, params)

    def create_index(self, table, columns: list, is_unique=True):
        self.exec("CREATE %s INDEX IF NOT EXISTS %s_index ON %s (%s)" % (
            "UNIQUE" if is_unique else "",
            "_".join(columns + ["unique"] if is_unique else columns),
            table,
            ",".join(columns)
        ))

    def get_type(self, dtype):
        if dtype is numpy.float:
            return "REAL"
        elif dtype in [numpy.int, numpy.bool]:
            return "INT"
        else:
            return "TEXT"

    def create_table(self, tab_name, fields: dict):
        _fields = dict()
        for name, dtype in fields.items():
            _fields[name] = self.get_type(dtype)

        self.exec("CREATE TABLE IF NOT EXISTS %s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,%s)"
                  % (tab_name, "".join(["%s %s," % (name, dtype) for name, dtype in _fields.items()])[:-1]))

    def replace(self, table, fields: dict):
        columns = []
        values = []

        for column, value in fields.items():
            columns.append(column)
            values.append(value)

        self.exec(
            "REPLACE INTO %s (%s) VALUES (%s)" % (
                table,
                ",".join(columns),
                ",".join(["?"] * len(values))
            ),
            *values
        )

    def drop(self, table):
        self.exec("DROP TABLE %s" % table)

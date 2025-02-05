import sqlite3

from .record import Record
from .utils import singularize

class Table:

    def __init__(self, connection: sqlite3.Connection, name: str):
        self.connection: sqlite3.Connection = connection
        self.name: str = name

    def create(self, columns: list):
        columns_str: str = ''
        for column in columns:
            columns_str += f'{column[0]} {column[1]}, '         
        sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
            id integer PRIMARY KEY, 
            {columns_str.rstrip(', ')}
        )''' # May want to replace string with list and use join
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            print(f'=> table="{self.name}", created\n')
        except sqlite3.Error as e:
            print(e)

    def list(self) -> list:
        sql:str = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.connection.execute(sql)
        table_arr = [table[0] for table in tables.fetchall()]
        print(f'=> tables={table_arr}\n')
        return table_arr

    def columns(self) -> list:
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({self.name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            # print(f'=> table="{self.name}", columns={column_names}\n')
            return column_names
        except sqlite3.Error as e:
            print(e)
            return []
        
    def read(self) -> list:
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {self.name}')
            rows = cursor.fetchall()
            print(f'=> table="{self.name}", records=[')
            for row in rows:
                print(f'...{row}')
            print(']\n')
            return rows
        except sqlite3.Error as e:
            print(e)
            return []

    def drop(self) -> None:
        sql: str = f'DROP TABLE IF EXISTS {self.name}'
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            print(f'=> table="{self.name}", dropped\n')
        except sqlite3.Error as e:
            print(e)

    def filter(self, column, value):
        return [val for val in self.read if val[column] == value]

    def join(self, obj):
        selector_arr = []
        join_arr = []

        try:
            for key in obj.keys():
                join_arr.append(f'JOIN {key} ON {self.name}.{singularize(key)}_id = {key}.id')
                for value in obj[key]:
                    selector_arr.append(f'{key}.{value}')
            sql: str = f"SELECT {', '.join(selector_arr)} FROM {self.name} {' '.join(join_arr)}"
            return self.connection.cursor().execute(sql).fetchall()
        except sqlite3.Error as e:
            print(e)

    @property
    def record(self):
        return Record(self.connection, table=self)
import sqlite3

from .record import Record
from .utils import singularize

class Table:

    def __init__(self, db, name: str) -> None:
        self.connection: sqlite3.Connection = db.connection
        self.db = db
        self.name: str = name

    def create(self, columns: list):
        columns_str: str = ''
        for column in columns:
            columns_str += f'{column[0]} {column[1]}, '         
        sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
            id integer PRIMARY KEY, 
            {columns_str.rstrip(', ')}
        )''' # May want to replace string with list and use join
        cursor = self.connection.cursor()
        cursor.execute(sql)
        print(f'=> table="{self.name}", created\n' if self.db.cli_logger else '')

    def list(self) -> list:
        sql:str = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.connection.execute(sql)
        table_arr = [table[0] for table in tables.fetchall()]
        print(f'=> tables={table_arr}\n' if self.db.cli_logger else '')
        return {'tables': table_arr} if self.db.return_dict else table_arr

    def columns(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        print(f'=> table="{self.name}", columns={column_names}\n' if self.db.cli_logger else '')
        return {'columns': column_names} if self.db.return_dict else column_names
        
    def read(self) -> list:
        columns = self.columns()['columns']
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.name}')
        rows = cursor.fetchall()
        if self.db.cli_logger:
            print(f'=> table="{self.name}", records=[')
            for row in rows:
                print(f'...{row}')
            print(']\n')

        data = {self.name: []}
        for row in rows:
            data[self.name].append({
                columns[i]: row[i] for i in range(len(row))
            })
        return data if self.db.return_dict else rows

    def drop(self) -> None:
        sql: str = f'DROP TABLE IF EXISTS {self.name}'
        cursor = self.connection.cursor()
        cursor.execute(sql)
        print(f'=> table="{self.name}", dropped\n' if self.db.cli_logger else '')

    def filter(self, column, value):
        return [val for val in self.read if val[column] == value]

    def join(self, obj):
        selector_arr = []
        join_arr = []

        for key in obj.keys():
            join_arr.append(f'JOIN {key} ON {self.name}.{singularize(key)}_id = {key}.id')
            for value in obj[key]:
                selector_arr.append(f'{key}.{value}')
        sql: str = f"SELECT {', '.join(selector_arr)} FROM {self.name} {' '.join(join_arr)}"
        return self.connection.cursor().execute(sql).fetchall()

    @property
    def record(self):
        return Record(table=self, db=self.db)
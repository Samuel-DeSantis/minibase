import sqlite3

from .record import Record

class Table:

    def __init__(self, connection, name: str):
        self.connection = connection
        self.name = name

    def create(self, columns: list):
        columns_str = ''
        for column in columns:
            columns_str += f'{column[0]} {column[1]}, '         
        sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
            id integer PRIMARY KEY, 
            {columns_str.rstrip(', ')}
        )'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            print(f'=> table="{self.name}", created\n')
        except sqlite3.Error as e:
            print(e)

    @property
    def list(self) -> list:
        tables = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_arr = [table[0] for table in tables.fetchall()]
        print(f'=> tables={table_arr}\n')
        return table_arr

    @property
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
        
    @property
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

    @property
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

    def join(self, table1, table2):
        table1 = {item[0]: item for item in table1}
        table2 = {item[0]: item for item in table2}
        return [(join[0], table1[join[1]], table2[join[2]]) for join in self.read]

    @property
    def record(self):
        return Record(self.connection, table=self)
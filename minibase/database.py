import os
import sqlite3

from .config import Configuration
from .table import Table

class Database(Configuration):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connection = self.connect_to(f"{self.db_file}.db")

    def connect_to(self, file: str) -> sqlite3.Connection:
        if self.cli_logger:
            print('--------------------------')
            print(f'Connected to "{file}"')
            print(f'SQLITE3_VERSION={sqlite3.sqlite_version}')
            print('--------------------------')
        return sqlite3.connect(file, check_same_thread=False)
    
    def disconnect(self) -> None:
        self.connection.close()
        print('=> database disconnected' if self.cli_logger else '')
        return None
    
    def delete(self, db_file: str) -> None:
        if db_file == f"{self.name}.db":
            self.disconnect
            os.remove(f'{self.name}.db')
        print('=> database deleted' if self.cli_logger else '')
        return None
    
    def SQL(self, sql: str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        if 'INSERT' in sql:
            self.connection.commit()
            return cursor.lastrowid
        elif 'WHERE' in sql:
            return cursor.fetchone()
        elif 'SELECT' in sql:
            return cursor.fetchall()
        return None
        
    def table(self, name: str = None) -> Table:
        return Table(b=self, name=name)
    
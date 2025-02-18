import os
import sqlite3

from .config import Configuration
from .table import Table

class Database(Configuration):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connection = self.connect_to(f"{self.db_file}.db")

    def connect_to(self, file: str) -> sqlite3.Connection:
        return sqlite3.connect(file, check_same_thread=False)
    
    def disconnect(self) -> None:
        self.connection.close()
    
    def delete(self, file: str) -> None:
        if file == self.db_file:
            self.disconnect
            os.remove(f'{self.db_file}.db')
    
    def SQL(self, sql: str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        if 'INSERT' in sql:
            self.connection.commit()
            return cursor.lastrowid
        else:
            return cursor.fetchall()
        
    def table(self, name: str = None) -> Table:
        return Table(db=self, name=name)
    
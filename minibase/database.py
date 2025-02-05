import sqlite3
import os

from .table import Table

class Database:

    def __init__(self, db_file: str = 'sqlite3'):
        self.connection = self.connect_to(f"{db_file}.db")
        self.name = db_file

    def connect_to(self, file: str) -> sqlite3.Connection:
        try:
            print('--------------------------')
            print(f'Connected to "{file}"')
            print(f'SQLITE3_VERSION={sqlite3.sqlite_version}')
            print('--------------------------')
            return sqlite3.connect(file)
        except sqlite3.Error as e:
            print(e)
            return None
    
    def disconnect(self) -> None:
        self.connection.close()
        print('=> database disconnected')
        return None
    
    def delete(self, db_file: str) -> None:
        if db_file == f"{self.name}.db":
            self.disconnect
            os.remove(f'{self.name}.db')
        print('=> database deleted')
        return None
    
    def SQL(self, sql: str):
        try:
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
        except sqlite3.Error as e:
            print(e)
        
    def table(self, name: str = None) -> Table:
        return Table(self.connection, name)
    
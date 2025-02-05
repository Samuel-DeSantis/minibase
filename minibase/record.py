import sqlite3

class Record:

    def __init__(self, connection: sqlite3.Connection, table):
            self.connection: sqlite3.Connection = connection
            self.table = table

    def create(self, record: list):
        columns: list = self.table.columns()[1:]
        sql: str = f'''INSERT INTO {self.table.name} ({', '.join(columns).rstrip(', ')}) VALUES({('?,' * len(columns)).rstrip(', ')})'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, record)
            self.connection.commit()
            print(f'=> table="{self.table.name}", record={record}\n')
            return cursor.lastrowid
        except sqlite3.Error as e:  
            print(e)
            return None
        
    def read(self, id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {self.table.name} WHERE id = ?', str(id))
            rows:tuple = cursor.fetchone()
            print(f'=> table="{self.table.name}", record={rows}\n')
            return rows
        except sqlite3.Error as e:
            print(e)
            return []
        
    def update(self, id: int, attributes: list, record: list):
        sql = f'''UPDATE {self.table.name} SET {', '.join([f'{column} = ?' for column in attributes])} WHERE id = ?'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, record + [id])
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def delete(self, id: int):
        sql: str = f'''DELETE FROM {self.table.name} WHERE id = ?'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (str(id),))
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)
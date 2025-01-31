# import sqlite3
import code
# from .database import Database

def ex(db):
    # Create Table
    db.table('users').create(
        columns=[
            ['name', 'text'], 
            ['level', 'integer']
        ])
    
    # List Tables
    db.table().list

    # List Columns
    db.table('users').columns

    # Create Records
    db.table('users').record.create(record=['John', 1])
    db.table('users').record.create(record=['Jane', 2])
    db.table('users').record.create(record=['Sean', 3])
    db.table('users').record.create(record=['Bill', 2])
    db.table('users').record.create(record=['Dan', 1])

    # Read Records
    db.table('users').read

    #Update Record
    db.table('users').record.update(
        id=4, 
        attributes=['name'], 
        record=['William']
    )

    # Read Record
    db.table('users').record.read(id=4)

    # Read Records
    db.table('users').read

    # Delete Record
    db.table('users').record.delete(id=5)

    # Read Records
    db.table('users').read

    # Drop Table
    db.table('users').drop # Drop Table

# Database Management System
def main() -> None:

    # Initialize Database
    # db = Database()
    code.interact(local=locals())
    # ex(db)

if __name__ == '__main__':
    main()



# class Database:
#     """
#     A class used to represent a Database connection.
    
#     Attributes
#     ----------
#     connection : sqlite3.connection
#         The connection object to the SQLite database.

#     Methods
#     -------
#     __init__(db_file: str = 'sqlite3')
#         Initializes the Database object and establishes a connection to the specified SQLite database file.

#     connect_to(file: str)
#         Attempts to connect to the specified SQLite database file and returns the connection object.

#     table(name: str = None)
#         Returns a Table object associated with the current database connection.
#     """

#     def __init__(self, db_file: str = 'sqlite3'):
#         self.connection = self.connect_to(f"{db_file}.db")

#     def connect_to(self, file: str) -> sqlite3.Connection:
#         try:
#             print('--------------------------')
#             print(f'Connected to "{file}"')
#             print(f'SQLITE3_VERSION={sqlite3.sqlite_version}')
#             print('--------------------------')
#             return sqlite3.connect(file)
#         except sqlite3.Error as e:
#             print(e)
#             return None
        
#     def table(self, name: str = None):
#         return Table(self.connection, name)
    
# class Table:
#     """
#     A class used to represent a Table in a SQLite database.
    
#     Attributes
#     ----------
#     connection : sqlite3.connection
#         A connection object to the SQLite database.

#     name : str
#         The name of the table.

#     Methods
#     -------
#     create(columns: list[tuple[str, str]]):
#         Creates the table with the specified columns if it does not already exist.

#     list() -> list[str]:
#         Lists all tables in the database.

#     columns() -> list[str]:
#         Retrieves the column names of the table.

#     read() -> list[tuple]:
#         Reads all records from the table.

#     drop() -> None:
#         Drops the table if it exists.

#     record() -> Record:
#         Returns a Record object associated with the table.
#     """

#     def __init__(self, connection, name: str):
#         self.connection = connection
#         self.name = name

#     def create(self, columns: list[str, str]):
#         """
#         asd
#         """
#         columns_str = ''
#         for column in columns:
#             columns_str += f'{column[0]} {column[1]}, '         
#         sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
#             id integer PRIMARY KEY, 
#             {columns_str.rstrip(', ')}
#         )'''
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(sql)
#             print(f'=> table="{self.name}", created\n')
#         except sqlite3.Error as e:
#             print(e)

#     def list(self) -> list[str]:
#         tables = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         print(f'=> tables={[table[0] for table in tables.fetchall()]}\n')
#         return [table[0] for table in tables.fetchall()]

#     def columns(self) -> list:
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(f"PRAGMA table_info({self.name});")
#             columns = cursor.fetchall()
#             column_names = [column[1] for column in columns]
#             # print(f'=> table="{self.name}", columns={column_names}\n')
#             return column_names
#         except sqlite3.Error as e:
#             print(e)
#             return []
        
#     def read(self) -> list:
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(f'SELECT * FROM {self.name}')
#             rows = cursor.fetchall()
#             print(f'=> table="{self.name}", records=[')
#             for row in rows:
#                 print(f'...{row}')
#             print(']\n')
#             return rows
#         except sqlite3.Error as e:
#             print(e)
#             return []

#     def drop(self) -> None:
#         sql: str = f'DROP TABLE IF EXISTS {self.name}'
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(sql)
#             print(f'=> table="{self.name}", dropped\n')
#         except sqlite3.Error as e:
#             print(e)

#     @property
#     def record(self):
#         return Record(self.connection, table=self)
    
# class Record:
#     """
#     A class to manage CRUD operations for a database table.

#     Attributes
#     ----------
#     connection : sqlite3.connection
#         The connection object to the SQLite database.

#     table : Table
#         The table object representing the database table.
        
#     Methods
#     -------
#     create(record: list[str]) -> int:
#         Inserts a new record into the table.

#     read(id: int) -> list:
#         Retrieves a record from the table by its ID.

#     update(id: int, attributes: list[str], record: list[str]) -> None:
#         Updates an existing record in the table by its ID.

#     delete(id: int) -> None:
#         Deletes a record from the table by its ID.
#     """

#     def __init__(self, connection, table: Table):
#         self.connection = connection
#         self.table = table

#     def create(self, record: list):
#         columns = self.table.columns()[1:]
#         sql = f'''INSERT INTO {self.table.name} ({', '.join(columns).rstrip(', ')}) VALUES({('?,' * len(columns)).rstrip(', ')})'''
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(sql, record)
#             self.connection.commit()
#             print(f'=> table="{self.table.name}", record={record}\n')
#             return cursor.lastrowid
#         except sqlite3.Error as e:  
#             print(e)
#             return None
        
#     def read(self, id: int):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(f'SELECT * FROM {self.table.name} WHERE id = ?', str(id))
#             rows = cursor.fetchone()
#             print(f'=> table="{self.table.name}", record={rows}\n')
#             return rows
#         except sqlite3.Error as e:
#             print(e)
#             return []
        
#     def update(self, id: int, attributes: list, record: list):
#         sql = f'''UPDATE {self.table.name} SET {', '.join([f'{column} = ?' for column in attributes])} WHERE id = ?'''
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(sql, record + [id])
#             self.connection.commit()
#         except sqlite3.Error as e:
#             print(e)

#     def delete(self, id: int):
#         sql = f'''DELETE FROM {self.table.name} WHERE id = ?'''
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(sql, (str(id),))
#             self.connection.commit()
#         except sqlite3.Error as e:
#             print(e)


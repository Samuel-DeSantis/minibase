from .record import Record
from .utils import singularize

class Table:

    def __init__(self, db, name: str) -> None:
        self.db = db
        self.name: str = name

    def create(self, columns: list) -> None:
        sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
            id integer PRIMARY KEY, 
            {', '.join([f'{column[0]} {column[1]}' for column in columns])}
        )'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql)

    def list(self) -> dict:
        tables = self.db.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return {'tables': [table[0] for table in tables.fetchall()]}

    def columns(self) -> dict:
        cursor = self.db.connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.name});")
        columns:list = cursor.fetchall()
        return {'columns': [column[1] for column in columns]}
        
    def read(self) -> dict:
        columns: list = self.columns()['columns']
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.name}')
        rows: tuple = cursor.fetchall()
        return {self.name: [dict(zip(columns, row)) for row in rows]}

    def drop(self) -> None:
        cursor = self.db.connection.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {self.name}')

    def filter(self, obj) -> dict:
        filter_params = [f'{key} = "{obj[key]}"' for key in obj.keys()]
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.name} WHERE {" AND ".join(filter_params)}')
        rows:tuple = cursor.fetchall()
        return {singularize(self.name): [dict(zip(self.columns()['columns'], row)) for row in rows]}

    def join(self, obj):
        selector_arr = [f'{key}.{value}' for key in obj.keys() for value in obj[key]]
        join_arr = [f'JOIN {key} ON {self.name}.{singularize(key)}_id = {key}.id' for key in obj.keys()]
        sql: str = f"SELECT {', '.join(selector_arr)} FROM {self.name} {' '.join(join_arr)}"
        rows = self.db.connection.cursor().execute(sql).fetchall()
        name = self.name if len(rows) > 1 else singularize(self.name)
        return {name: [dict(zip(selector_arr, row)) for row in rows]}

    @property
    def record(self):
        return Record(table=self, db=self.db)
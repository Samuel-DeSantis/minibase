from .utils import singularize

class Record:

    def __init__(self, db, table) -> None:
        self.db = db
        self.table = table

    def create(self, record: list) -> dict:
        columns: list = self.table.columns()['columns']
        sql: str = f'''INSERT INTO {self.table.name} ({', '.join(columns[1:]).rstrip(', ')}) VALUES({('?,' * len(columns[1:])).rstrip(', ')})'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, record)
        self.db.connection.commit()
        record.insert(0, cursor.lastrowid)
        return {singularize(self.table.name): dict(zip(columns, record))}
                
    def read(self, id: int) -> dict:
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.table.name} WHERE id = {id}')
        rows:tuple = cursor.fetchone()
        columns = self.table.columns()['columns']
        return {singularize(self.table.name): dict(zip(columns, rows))}
        
    def update(self, id: int, attributes: list, record: list) -> list:
        sql: str = f'''UPDATE {self.table.name} SET {', '.join([f'{column} = ?' for column in attributes])} WHERE id = ?'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, record + [id])
        self.db.connection.commit()
        return {singularize(self.table.name): {'id': id, 'record': [*record]}}

    def delete(self, id: int)-> None:
        sql: str = f'''DELETE FROM {self.table.name} WHERE id = ?'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, (str(id),))
        self.db.connection.commit()
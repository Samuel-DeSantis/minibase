class Record:

    def __init__(self, db, table) -> None:
        self.db = db
        self.table = table

    def create(self, record: list) -> tuple:
        columns: list = self.table.columns()['columns'][1:]
        sql: str = f'''INSERT INTO {self.table.name} ({', '.join(columns).rstrip(', ')}) VALUES({('?,' * len(columns)).rstrip(', ')})'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, record)
        self.db.connection.commit()
        return {'user': cursor.lastrowid} if self.db.cli_logger else cursor.lastrowid
                
    def read(self, id: int) -> tuple:
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.table.name} WHERE id = ?', str(id))
        rows:tuple = cursor.fetchone()
        return {'user': rows} if self.db.cli_logger else rows
        
    def update(self, id: int, attributes: list, record: list) -> list:
        sql: str = f'''UPDATE {self.table.name} SET {', '.join([f'{column} = ?' for column in attributes])} WHERE id = ?'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, record + [id])
        self.db.connection.commit()
        return {'user': [id, *record]} if self.db.cli_logger else [id, *record]

    def delete(self, id: int)-> None:
        sql: str = f'''DELETE FROM {self.table.name} WHERE id = ?'''
        cursor = self.db.connection.cursor()
        cursor.execute(sql, (str(id),))
        self.db.connection.commit()
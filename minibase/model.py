import sqlite3

class Model:
    name: str = None  # Subclasses should define this
    db: sqlite3.Connection = None  # Database connection

    def __init__(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)

    @classmethod
    def connect(cls, db) -> None:
        cls.db = db

    @classmethod
    def create(cls, columns: dict) -> None:
        sql = f'''CREATE TABLE IF NOT EXISTS {cls.name} (
            id INTEGER PRIMARY KEY, 
            {', '.join([f'{key} {value}' for key, value in columns.items()])}
        )'''
        cursor = cls.db.connection.cursor()
        cursor.execute(sql)
        cls.db.connection.commit()

    @classmethod
    def alter(cls, column: dict) -> None:
        for key, value in column.items():
            sql = f"ALTER TABLE {cls.name} ADD COLUMN {key} {value}"
            cursor = cls.db.connection.cursor()
            cursor.execute(sql)
            cls.db.connection.commit()

    @classmethod
    def columns(cls) -> list:
        cursor: sqlite3.Cursor = cls.db.connection.cursor()
        cursor.execute(f"PRAGMA table_info ({cls.name});")
        columns: list = cursor.fetchall()
        return [column[1] for column in columns]

    @classmethod
    def insert(cls, record: dict | list) -> dict:
        records = record if type(record) == list else [record]
        for record in records:
            sql: str = f'''INSERT INTO {cls.name} ({', '.join(record.keys())}) VALUES ({', '.join('?' * len(record.keys()))})'''
            cursor: sqlite3.Cursor = cls.db.connection.cursor()
            cursor.execute(sql, list(record.values()))
            cls.db.connection.commit()
        return records

    @classmethod
    def select(cls,
			where: dict = {},
			order: dict = {'by': []},
			limit: int = None
		) -> dict:
        sql: str = f"SELECT * FROM {cls.name}"
        if where:
            sql += ' WHERE ' + ' AND '.join([f'{key} = ?' for key in where.keys()])
        if order['by']:
            sql += ' ORDER BY ' + ', '.join(order['by']) + f" {'DESC' if 'descending' in order else ''}"
        if limit:
            sql += f" LIMIT {limit}"
        cursor: sqlite3.Cursor = cls.db.connection.cursor()
        cursor.execute(sql, list(where.values()))
        rows = cursor.fetchall()
        return [cls(**dict(zip(cls.columns(), row))) for row in rows]

    @classmethod
    def update(cls, set_values: dict, where: dict) -> None:
        sql: str = f'''UPDATE {cls.name} SET {', '.join([f'{key} = ?' for key in set.keys()])} WHERE {', '.join([f'{key} = ?' for key in where.keys()])}'''
        cursor: sqlite3.Cursor = cls.db.connection.cursor()
        cursor.execute(sql, list(set.values()) + list(where.values()))
        cls.db.connection.commit()

    @classmethod
    def delete(cls, id: int) -> None:
        sql: str = f'''DELETE FROM {cls.name} WHERE id = ?'''
        cursor: sqlite3.Cursor = cls.db.connection.cursor()
        cursor.execute(sql, (id,))
        cls.db.connection.commit()

    # Relationship: has_many
    def has_many(self, related_class, foreign_key):
        return related_class.select(where={foreign_key: self.id})

    # Relationship: belongs_to
    def belongs_to(self, related_class, foreign_key):
        related_id = getattr(self, foreign_key)
        return related_class.select(where={'id': related_id})[0] if related_id else None
    
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{key}={value}' for key, value in self.__dict__.items()])})"
import sqlite3

from utils import singularize

class Table:

	def __init__(self, db, name) -> None:
		self.db: sqlite3.Connection = db
		self.name: str = name

	def create(self, columns: dict) -> None:
		sql: str = f'''CREATE TABLE IF NOT EXISTS {self.name} (
			id integer PRIMARY KEY, 
			{', '.join([f'{key} {value}' for key, value in columns.items()])}
		)'''
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql)
		self.db.connection.commit()

	def alter(self, column: dict) -> None:
		for key, value in column.items():
			sql: str = f"ALTER TABLE {self.name} ADD COLUMN {key} {value}"
			cursor: sqlite3.Cursor = self.db.connection.cursor()
			cursor.execute(sql)
			self.db.connection.commit()

	def rename(self, new_name: str) -> None:
		sql: str = f"ALTER TABLE {self.name} RENAME TO {new_name}"
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql)
		self.db.connection.commit()

	def columns(self) -> list:
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(f"PRAGMA table_info ({self.name});")
		columns: list = cursor.fetchall()
		return [column[1] for column in columns]
	
	def insert(self, record: dict | list) -> dict:
		records = record if type(record) == list else [record]
		for record in records:
			sql: str = f'''INSERT INTO {self.name} ({', '.join(record.keys())}) VALUES ({', '.join('?' * len(record.keys()))})'''
			cursor: sqlite3.Cursor = self.db.connection.cursor()
			cursor.execute(sql, list(record.values()))
			self.db.connection.commit()
		return records
	
	def select(self,
			where: dict = {},
			order: dict = {'by': []},
			limit: int = None
		) -> dict:
		sql: str = f"SELECT * FROM {self.name}"
		if where:
			sql += ' WHERE ' + ' AND '.join([f'{key} = ?' for key in where.keys()])
		if order['by']:
			sql += ' ORDER BY ' + ', '.join(order['by']) + f" {'DESC' if 'descending' in order else ''}"
		if limit:
			sql += f" LIMIT {limit}"
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql, list(where.values()))
		users = cursor.fetchall()
		return {self.name: [dict(zip(self.columns(), user)) for user in users]} 

	def update(self, set: dict, where: dict) -> None:
		sql: str = f'''UPDATE {self.name} SET {', '.join([f'{key} = ?' for key in set.keys()])} WHERE {', '.join([f'{key} = ?' for key in where.keys()])}'''
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql, list(set.values()) + list(where.values()))
		self.db.connection.commit()

	def delete(self, id: int) -> None:
		sql: str = f'''DELETE FROM {self.name} WHERE id = ?'''
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql, (id,))
		self.db.connection.commit()

	def join(self, selection: dict = {}) -> list:
		selection_str: str = '*' if selection == {} else ', '.join([f"{table}.{col}" for table, cols in selection.items() for col in (cols if isinstance(cols, list) else [cols])])
		join_str: str = ' '.join([f"JOIN {key} ON {self.name}.{singularize(key)}_id = {key}.id" for key in selection.keys() if key != self.name])
		sql: str = f"SELECT {selection_str} FROM {self.name} {join_str}"
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return {self.name: [dict(zip(selection_str.split(', '), row)) for row in rows]}

	def drop(self) -> None:
		sql: str = f"DROP TABLE IF EXISTS {self.name}"
		cursor: sqlite3.Cursor = self.db.connection.cursor()
		cursor.execute(sql)
		self.db.connection.commit()
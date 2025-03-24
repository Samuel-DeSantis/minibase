import sqlite3
import os

from configuration import Configuration
from table import Table

class Minibase(Configuration):

	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)

	def tables(self) -> list:
		tables: sqlite3.Cursor = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
		return [table[0] for table in tables.fetchall()]

	def disconnect(self) -> None:
		self.connection.close()
		self.connection = None

	def delete(self, file: str) -> None:
		if file == self.db_file:
			os.remove(f'{self.db_file}.db')

	def SQL(self, sql: str) -> list:
		cursor: sqlite3.Cursor = self.connection.cursor()
		cursor.execute(sql)
		if 'INSERT' in sql:
			self.connection.commit()
			return cursor.lastrowid
		else:
			return cursor.fetchall()
		
	def table(self, name: str = None) -> Table:
		return Table(db=self, name=name)
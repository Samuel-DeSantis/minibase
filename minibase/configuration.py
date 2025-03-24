import sqlite3

class Configuration:
  
	def __init__(self,
			db_file: str = 'sqlite3',
			type: dict = {'database': 'sqlite3'},
			logging: bool = False
		) -> None:
		self.db_file: str = db_file
		self.type = type
		self.logging: bool = logging
		self.connection = self.database()

	def database(self) -> sqlite3.Connection:
		match(self.type['database']):
			case 'sqlite3':
				return sqlite3.connect(f"{self.db_file}.db", check_same_thread=False)
			case 'postgresql':
				# return psycopg2.connect(
				#	database=self.type['database'],
				#	user=self.type['user'],
				#	password=self.type['password'],
				#	host=self.type['host'],
				#	port=self.type['port']
				# )
				raise Exception('PostgreSQL support is not implemented yet')
			case _:
				raise Exception('Unsupported database type')
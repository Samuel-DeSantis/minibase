'''
Configuration for Database

Attributes:
	db_file: str = 'sqlite3'
		Sets the name for the db.file to be accessed or created.
	
	cli_logger: bool = False
		Enables logging for the CLI.

	return_dict: bool = True
		Returns data in dictionary format.
'''

class Configuration:
	def __init__(self,
			db_file: str = 'sqlite3',
			cli_logger: bool = False,
			return_dict: bool = True,
			**kwargs,
		) -> None:
		self.db_file = db_file
		self.cli_logger = cli_logger
		self.return_dict = return_dict
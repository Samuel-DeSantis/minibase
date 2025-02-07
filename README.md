# Minibase

Minibase is a simple SQLite3 package for creating and operating on a SQL database.

## Authors and Acknowledgments
- **Author:** Samuel DeSantis
- **Contributors:** ✌️Waiting

## License
Minibase is licensed under MIT License.

## Contents
1. [Installation](#installation)
2. [Usage](#usage)
    1. [Database](#database)
        1. [Initialize Database](#initialize-database)
        2. [Disconnect Database](#disconnect-database)
        3. [Delete Database](#delete-database)
    2. [Tables](#tables)
        1. [Create Table](#create-table)
        2. [Read Records](#read-records)
        3. [List Tables](#list-tables)
        4. [List Columns](#list-columns)
        5. [Drop Table](#drop-table)
    3. [Records](#records)
        1. [Create](#create)
        2. [Read](#read)
        3. [Update](#update)
        4. [Delete](#delete)
3. [Example](#example)
4. [Documentation](#documentation)

## Installation
minibase currently in testing on TestPyPi.
```
pip install -i https://test.pypi.org/simple/ minibase
```

## Usage
The philosophy for the design of this library is subject based method chaining. This allows for a logical flow for the user and may be compared to a Supabase style of database interaction.

## Database

### Initialize Database:
See [configuration](#configuration) documentation for additional options.
```
import minibase
db = minibase.Database()
```

The database default name will be 'sqlite3.db', but can be renamed by providing any string.

```
db = Database('CompanyUsers')
```

### Disconnect Database:
Disconnect from the database when operations are complete, not necessary, but good practice.
```
db.disconnect()
```

### Delete Database:
Delete an existing database file. Required to type the name of the database before the deletion is executed.
```
db.delete()
```

### SQL:
The SQL method allows the user to write plain SQL to execute with the database. ORM's allow for convenience with abstraction at the cost of precision.
```
db.SQL('SELECT * FROM users WHERE id = 1')
```

## Tables

### Create Table:
Create a `users` table with `name`, `level`, and `title` text columns.
```
db.table('users').create(
    columns=[
        ['name', 'text'],
        ['level', 'text'],
        ['title', 'text']
    ]
)
```

### Read Records:
Returns a list of all table records.
```
db.table('users').read()
> {'users': [<record_1>, <record_2>, <record_3>,]}
```

### List Tables:
Returns a list of all tables in the respective database.
```
db.table().list()
> {'tables': ['users',]}
```

### List Columns:
Returns a list of all columns in the respective table.
```
db.table('users').columns()
> {'columns': ['name', 'level', 'title']}
```

### Drop Table:
Drops the specified table.
```
db.table('users').drop()
```

### Filter
Filters specified column by given value. Column position is required to be an integer value (ex. [0]=Primary Key, [1]='name', [2]='level, etc.).
```
db.table('users').filter(<column position>, <value>)
```

### Join
The join method is meant to populate join tables with the respective objects of reference. Replacing the primary keys with a tuple of the actual object. Below, 'user_projects' represents a table with user_id and project_id columns.
```
db.table('user_projects').join({
    'users': ['first_name', 'last_name', 'username'],
    'projects': ['name'],
})
```

## Records
The record class has the standard CRUD functionality and should be self explanatory. All methods are chained following a a record object.

### Create:
```
db.table('users').record.create(['John Doe', 2, 'Engineer'])
```

### Read:
```
db.table('users').record.read(id=1)
> {'user': <record>}
```

### Update:
```
db.table('users').record.update(
    id=1,
    attributes=['name']
    record=['William']
)
```

### Delete:
```
db.table('users').record.delete(id=5)
```

## Example
Below is an example of how to use minibase in an application.
```
import minibase

# Create and connect to'sqlite3.db'
db = minibase.Database() 

# Create users table with name:text and age:integer attributes
db.table('users').create(columns=[
    ['name', 'text'],
    ['age', 'integer']
])

# Create 3 new user records
db.table('users').record.create(['Michael Scott', 59])
db.table('users').record.create(['Dwight Schrute', 55])
db.table('users').record.create(['Andy Bernard', 41])

# Read users table
db.table('users').read()

# Update user record
db.table('users').record.update(
    id=1, 
    attributes=['name'], 
    record=['Michael Scarn']
)

# Delete user record
db.table('users').record.delete(id=3)

# Read users table
db.table('users').read()
```

## Documentation

### Configuration
Sets configuration values for the database.

```
Configuration for Database

Attributes:
	db_file: str = 'sqlite3'
		Sets the name for the db.file to be accessed or created.
	
	cli_logger: bool = False
		Enables logging for the CLI.

	return_dict: bool = True
		Returns data in dictionary format.
```

### Database
A class used to represent a Database connection.
```
Attributes
----------
connection : sqlite3.connection
    The connection object to the SQLite database.

Methods
-------
__init__(db_file: str = 'sqlite3')
    Initializes the Database object and establishes a connection to the specified SQLite database file.

connect_to(file: str)
    Attempts to connect to the specified SQLite database file and returns the connection object.

disconnect()
    Disconnects the connection to the database.

delete()
    Deletes the database file after user input confirmation.

table(name: str = None)
    Returns a Table object associated with the current database connection.
```

### Table
A class used to represent a Table in a SQLite database.
```
Attributes
----------
connection : sqlite3.connection
    A connection object to the SQLite database.

name : str
    The name of the table.

Methods
-------
create(columns: list[tuple[str, str]]):
    Creates the table with the specified columns if it does not already exist.

list() -> list[str]:
    Lists all tables in the database.

columns() -> list[str]:
    Retrieves the column names of the table.

read() -> list[tuple]:
    Reads all records from the table.

drop() -> None:
    Drops the table if it exists.

record() -> Record:
    Returns a Record object associated with the table.
```

### Record
A class to manage CRUD operations for a database table.
```
Attributes
----------
connection : sqlite3.connection
    The connection object to the SQLite database.

table : Table
    The table object representing the database table.
    
Methods
-------
create(record: list[str]) -> int:
    Inserts a new record into the table.

read(id: int) -> list:
    Retrieves a record from the table by its ID.

update(id: int, attributes: list[str], record: list[str]) -> None:
    Updates an existing record in the table by its ID.

delete(id: int) -> None:
    Deletes a record from the table by its ID.
```
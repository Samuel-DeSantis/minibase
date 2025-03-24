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
        2. [View Tables](#view-tables)
        3. [Disconnect Database](#disconnect-database)
        4. [Delete Database](#delete-database)
        5. [Custom SQL](#custom-sql)
    2. [Tables](#tables)
        1. [Create Table](#create-table)
        2. [Alter Table](#alter-table)
        3. [Rename Table](#rename-table)
        4. [Insert Record](#insert-record)
        5. [Read Records](#read-records)
        6. [Update Record](#update-record)
        7. [Delete Record](#delete-record)
        8. [Drop Table](#drop-table)
    3. [Authorization](#authorization)
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
from minibase import Minibase
db = Minibase()
```

The database default name will be 'sqlite3.db', but can be renamed by providing any string.

```
db = Minibase('CompanyUsers')
```

### View Tables
View the tables that currently exist in the database.
```
db.tables()
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

### Custom SQL:
The SQL method allows the user to write plain SQL to execute with the database. ORM's allow for convenience with abstraction at the cost of precision.
```
db.SQL('SELECT * FROM users WHERE id = 1')
```

## Tables

### Create Table:
Create a `users` table with `username`, `name`, and `password_digest` text columns.
```
db.table('users').create(
    columns={
        'username': 'text NOT NULL UNIQUE'
        'name': 'text'
        'password_digest': 'text NOT NULL'
    }
)
```

### Alter Table
Add a new column to an existing table.
```
db.table('users').alter(
    columns={
        'email': 'text NOT NULL'
    }
)
```

### Rename Table
```
db.table('users').rename('people')
```

### List Columns:
Returns a list of all columns in the respective table.
```
db.table('users').columns()
> ['username', 'name', 'email', 'password_digest']
```

### Insert Record
Add a record or multiple records to the table.
```
db.table('users').insert({
    'username': 'mscott',
    'name': 'Michael Scott',
    'email': 'mscott@email.com',
    'password_digest': '********'
})

db.table('users').insert([
    {
        'username': 'dschrute',
        'name': 'Dwight Schrute',
        'email': 'dschrute@email.com',
        'password_digest': '********'
    },
    ...
    {
        'username': 'mscarn',
        'name': 'Michael Scarn',
        'email': 'mscarn@email.com',
        'password_digest': '********'
    }
])

```

### Read Records:
Returns a list of all table records.
```
db.table('users').select()
```
Query options are available as arugments for the select method. The query below sets a maximum limit of 5 records, is looking for only records with the name of 'John', and to order the returned records by their username in descending order, with ascending as default.
```
db.table('users').select(
    where={'name': 'John'},
    order={
        'by': ['username'],
        'descending': True
    },
    limit=5
)
```
All select queries are returned as a dictionary with the key of the name of the table.
```
> {'users': [<record_1>, <record_2>, <record_3>,]}
```

### Update Record
Update an existing record.
```
db.table('users').update(
    set={'email': 'threatlevelmidnight@email.com'},
    where={'name': 'Michael Scarn'}
)
```

### Delete Record
```
db.table('users').delete(id=3)
```

### Join Table
```
db.table('author_articles').join(
    selection={
        'authors': 'name',
        'articles': ['title', 'content']
    }
)
```

### Drop Table:
Drops the specified table.
```
db.table('users').drop()
```

## Authorization
The Minibase Authorization class helps to hash and check hashed passwords.
```
from minibase import Authorization

auth = Authorization()
password_digest = auth.hash('password')
auth.check('passord', password_digest)
```

## Examples

See here for an example using minibase with a simple flask web app: [Minibase Flask Example](https://github.com/Samuel-DeSantis/minibase-flask-example)

Below is an example of how to use minibase in an application.
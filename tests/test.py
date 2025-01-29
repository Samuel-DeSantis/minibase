import code
import os
from database import Database

def test_create_table(db):
    print('Creating table...')
    db.table('users').create([
        ('name', 'TEXT'),
        ('email', 'TEXT'),
        ('age', 'INTEGER')
    ])
    print('Table created.')
    print('Asserting table columns...')
    assert db.table('users').columns == ['id', 'name', 'email', 'age']
    print('Table columns asserted.')
    print('--------------------')

def test_list_tables(db):
    print('Listing tables...')
    assert db.table().list == ['users']
    print('Tables listed.')
    print('--------------------')

def test_create_record(db):
    print('Creating record...')
    db.table('users').record.create(['John', 'john@email.com', 25])
    print('Record created.')
    assert db.table('users').read == [(1, 'John', 'john@email.com', 25)]
    print('Record asserted.')
    print('--------------------')

def test_drop_table(db):
    print('Dropping table...')
    db.table('users').drop
    assert db.table().list == []
    print('Table dropped.')
    print('--------------------')


def disconnect_and_remove_db(db):
    db.connection.close()
    os.remove('test.db')

def main():
    db = Database('test')

    test_create_table(db)
    test_list_tables(db)
    test_create_record(db)
    test_drop_table(db)

    # code.interact(local=locals())
    disconnect_and_remove_db(db)
   

if __name__ == '__main__':
    main()

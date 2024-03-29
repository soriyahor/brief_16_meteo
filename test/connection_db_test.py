from functions.connection_db import connect_db

def test_connect_db():
    assert connect_db(dbname='postgres', user='postgres', password='soriya') == conn
    assert connect_db(dbname='postgres', user='postgres', password='password') == None
    assert connect_db(dbname='postgres', user='user', password='soriya') == None
    assert connect_db(dbname='dbname', user='postgres', password='soriya') == None




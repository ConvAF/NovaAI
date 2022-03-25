import sqlite3

import pytest
from chatbot.db import get_db

def test_get_close_db(app):
    """ Test getting and closing the db """
    with app.app_context():
        db = get_db()
        # Same connection is returned every time
        assert db is get_db()

    # Connection can be queried and closes successfuly
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """ Test the initialization of the db """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # The init-db command can be invoked
    monkeypatch.setattr('chatbot.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output
    assert Recorder.called


def test_user_schema(app):
    """ Test the schema of the user table """
    with app.app_context():
        db = get_db()
    
        # There exist users in the database
        row = db.execute("select * from user").fetchone()
        
        # Database has correct columns
        cols = ['name', 'email', 'password']
        for col in cols:
            assert(col in row.keys())


import sqlite3

import click
import flask
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app: flask.app.Flask):
    """ Initialize an application.

    Registers the db related commands in the app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    """ Initialize the database.

    Initializes the database according
    to the proivded schema.    
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

# Define a command line command 'init-db'
@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


def get_db() -> sqlite3.Connection:
    """ Return the database object.

    If not already connected to the database,
    establishes connection, stores it in the
    g object and returns the db.

    Returns:
    --------
     - g.db: sqlite3.Connection
        The connection to the database
    """
    # g stores info about the request
    # current_app refers to the 
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dicts (key is col name)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e: BaseException = None):
    """ Closes the connection to the database.

    Called after each request.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()



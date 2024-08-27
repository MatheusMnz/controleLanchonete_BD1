# db_utils.py
from flask import g
import sqlite3
from config import DATABASE

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db_connection():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db_connection(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

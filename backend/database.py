import sqlite3
import os
from flask import g
from config import Config

def get_db():
    """Get database connection for the current application context."""
    if 'db' not in g:
        db_path = Config.DATABASE_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return g.db

def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app=None):
    """Initialize the database with the schema.sql file."""
    schema_path = os.path.join(Config.BASE_DIR, 'database', 'schema.sql')
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    if os.path.exists(schema_path):
        with open(schema_path, mode='r', encoding='utf-8') as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)

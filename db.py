# db.py

import sqlite3
from flask import g 

def init_db(app):
    
    def get_db():
        db = getattr(g, 'db', None)
        if db is None:
            db = sqlite3.connect(app.config['DATABASE_NAME'])
        return db
    
    @app.teardown_appcontext 
    def close_connection(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()
            
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
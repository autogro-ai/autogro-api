# db.py
from flask import g
import mysql.connector
from config import Config

def get_db():
    if 'db' not in g:
        db = mysql.connector.connect(
            host=Config.dbHostName,
            port=Config.dbPortNumber,
            user=Config.dbUser,
            password=Config.dbPassword, 
            database=Config.dbName
        )
    return db
def get_db_OG():
    
    if 'dbog' not in g:
        dbog = mysql.connector.connect(
            host=Config.dbHostName,
            port=Config.dbPortNumber,
            user=Config.dbOGUser,
            password=Config.dbOGPassword, 
            database=Config.dbOGName
        )
    return dbog

def close_db(db):
    db.close()

def close_dbog(db):
    db.close()    
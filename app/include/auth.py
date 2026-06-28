from include import db
from flask import Flask, session, current_app
import mysql.connector, hashlib, os

def create_account(app, username, password):
    database = app.db
    cursor = database.cursor(dictionary=True, buffered=True)

    cursor.execute(''' SELECT * FROM USERS WHERE username=%s AND password=%s ''', (username, hashlib.sha3_256(password.encode()).hexdigest()))
    result = cursor.fetchall()

    if not (len(result)>0):
        cursor.execute(''' INSERT INTO USERS (username, password) VALUES (%s, %s) ''', (username, hashlib.sha3_256(password.encode()).hexdigest()))
        database.commit()
        return True
    else:
        return False

def user_auth(app, username, password):
    if(session.get('user')):
        return True

    database = app.db
    cursor = database.cursor(dictionary=True, buffered=True)
    
    cursor.execute(''' SELECT * FROM USERS''')
    result = cursor.fetchall()

    if(len(result)==0):
        create_account(app, username, password)

    cursor.execute(''' SELECT * FROM USERS WHERE username=%s AND password=%s ''', (username, hashlib.sha3_256(password.encode()).hexdigest()))
    result = cursor.fetchall()

    if(len(result)>0):
        session['user'] = result[0]
        return True
    else:
        return False
from include import db, context
from flask import Flask, session, current_app
import mysql.connector, hashlib, os
import feedparser

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

def initial_setup(app, username, password):
    create_account(app, username, password)
    database = app.db
    cursor = database.cursor(dictionary=True, buffered=True)

    rss_urls = ["https://feeds.bbci.co.uk/news/rss.xml"]

    for url in rss_urls:      
        cursor.execute(''' INSERT INTO SUBSCRIPTIONS (USER_ID, rss_link) VALUES (1, %s) ''', [str(url)])
        database.commit()
    
    app.ctx = context.get_context(app)

def user_auth(app, username, password):
    if(session.get('user')):
        return True

    database = app.db
    cursor = database.cursor(dictionary=True, buffered=True)
    
    cursor.execute(''' SELECT * FROM USERS''')
    result = cursor.fetchall()

    if(len(result)==0):
        initial_setup(app, username, password)

    cursor.execute(''' SELECT * FROM USERS WHERE username=%s AND password=%s ''', (username, hashlib.sha3_256(password.encode()).hexdigest()))
    result = cursor.fetchall()

    if(len(result)>0):
        session['user'] = result[0]
        return True
    else:
        return False
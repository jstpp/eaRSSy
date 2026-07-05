from include import db as database
from flask import session
import mysql.connector
import feedparser

def get_context(app):
    context = {'channels': []}
    result = []
    if(app.db):
        cursor = app.db.cursor(dictionary=True, buffered=True)
        cursor.execute(''' SELECT * FROM SUBSCRIPTIONS ''')
        result = cursor.fetchall()
        
    for channel in result:
        print(result)
        context['channels'].append(feedparser.parse(channel['rss_link']))
        context['channels'][-1]['SUBSCRIPTION_ID'] = channel['SUBSCRIPTION_ID']
    return context

def delete_channel(id, app):
    id = int(id)
    cursor = app.db.cursor(dictionary=True, buffered=True)
    cursor.execute(''' DELETE FROM SUBSCRIPTIONS WHERE SUBSCRIPTION_ID=%s ''', [id])
    app.db.commit()

    app.ctx = get_context(app)
    

def add_channel(url, app):
    try:
        test = feedparser.parse(url).feed.title
    except:
        pass
    else:
        cursor = app.db.cursor(dictionary=True, buffered=True)
        cursor.execute(''' INSERT INTO SUBSCRIPTIONS (USER_ID, rss_link) VALUES (%s, %s) ''', [session.get("user")['USER_ID'], url])
        app.db.commit()
        app.ctx = get_context(app)
    
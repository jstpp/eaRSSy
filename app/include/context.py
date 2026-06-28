from include import db as database
import mysql.connector
import feedparser

def get_context(rss_urls, app):
    context = {'channels': []}
    result = []
    db = app.db
    if(db):
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(''' SELECT * FROM SUBSCRIPTIONS ''')
        result = cursor.fetchall()
        
    for url in rss_urls:
        context['channels'].append(feedparser.parse(url))
    return context
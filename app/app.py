from flask import Flask, render_template, request, session
import os

import include.context as context
import include.auth as auth
import include.db as db

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'earssy_db'
app.config['MYSQL_PASSWORD'] = 'earssy_db'
app.config['MYSQL_DB'] = 'earssy_db'
#app.secret_key = os.getenv("EARSSY_SECRET_KEY")
app.secret_key = "oke92k30932k020e2e03e02ke0" # temporary
app.db = db.get_db(app)


rss_urls = ["https://feeds.bbci.co.uk/news/rss.xml",
            "https://www.polsatnews.pl/rss/swiat.xml"] # Temporary URLs for initial setup. Will be replaced by mysql database.

context = context.get_context(rss_urls, app) # Will be initialized with users' login

@app.route("/", methods=['GET'])
def site_main():
    return render_template('index.html', **context)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if(request.form.get('login_username', 'none')!='none' and request.form.get('login_password', 'none')!='none'):
        if(auth.user_auth(app, request.form.get('login_username', 'none'), request.form.get('login_password', 'none'))):
            return render_template('profile.html', **context)
    if(session.get("user")):
        return render_template('profile.html', **context)
    else:
        return render_template('login.html', **context)
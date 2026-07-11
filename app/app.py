from flask import Flask, render_template, request, session, redirect, url_for
import os

import include.context as context
import include.auth as auth
import include.db as db

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'earssy_db'
app.config['MYSQL_PASSWORD'] = 'earssy_db'
app.config['MYSQL_DB'] = 'earssy_db'
app.secret_key = os.getenv("EARSSY_SECRET_KEY")
app.db = db.get_db(app)

app.ctx = context.get_context(app)

@app.route("/", methods=['GET'])
def site_main():
    return render_template('index.html', **app.ctx)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if(request.form.get('login_username', 'none')!='none' and request.form.get('login_password', 'none')!='none'):
        if(auth.user_auth(app, request.form.get('login_username', 'none'), request.form.get('login_password', 'none'))):
            return render_template('profile.html', **app.ctx)
    if(session.get("user")):
        return render_template('profile.html', **app.ctx)
    else:
        return render_template('login.html', **app.ctx)

@app.route("/delete-channel", methods=['GET'])
def delete_channel():
    context.delete_channel(request.args.get('id', 'none'), app)
    return redirect(url_for('profile'))

@app.route("/add-channel", methods=['GET'])
def add_channel():
    context.add_channel(request.args.get('url', 'none'), app)
    return redirect(url_for('profile'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
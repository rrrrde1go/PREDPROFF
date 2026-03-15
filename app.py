from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from constants import SECRET_KEY
from datetime import timedelta


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=1)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['username']
        session['username'] = user
        return redirect(url_for('user'))
    else:
        if "username" in session:
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/user')
def user():
    if 'username' in session:
        user = session['username']
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/graph')
def graph():
    return render_template('graph.html')


if __name__ == "__main__":
    app.run(debug=True)

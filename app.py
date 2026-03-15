from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/graph')
def graph():
    return render_template('graph.html')


if __name__ == "__main__":
    app.run(debug=True)

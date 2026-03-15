from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("Name", db.String(45))
    surname = db.Column("Surname", db.String(45))
    login = db.Column("login", db.String(45), nullable = False, unique = True)
    password = db.Column('password', db.String(40))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
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

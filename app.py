from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from constants import SECRET_KEY
from datetime import timedelta

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        flash('Вы уже вошли!')
        return redirect(url_for('user'))

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Пользователь не найден!")
            return redirect(url_for('login'))

        session.permanent = True
        session['username'] = user.username
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name

        flash("Успешный вход!")
        return redirect(url_for('user'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        username = request.form['username'].strip().lower()

        if not first_name or not last_name or not username:
            flash("Все поля обязательны для заполнения!")
            return render_template('register.html',
                                   first_name=first_name,
                                   last_name=last_name,
                                   username=username)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует!")
            return render_template('register.html',
                                   first_name=first_name,
                                   last_name=last_name,
                                   username=username)

        new_user = User(first_name, last_name, username)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Произошла ошибка при регистрации. Попробуйте ещё раз.")
            return render_template('register.html',
                                   first_name=first_name,
                                   last_name=last_name,
                                   username=username)

        session.permanent = True
        session['username'] = username
        session['first_name'] = first_name
        session['last_name'] = last_name

        flash("Регистрация успешна! Вы вошли в систему.")
        return redirect(url_for('user'))

    return render_template('register.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' not in session:
        flash("Не выполнен вход в аккаунт!")
        return redirect(url_for('login'))

    first_name = session.get('first_name')
    last_name = session.get('last_name')
    username = session.get('username')

    return render_template('user.html',
                           first_name=first_name,
                           last_name=last_name,
                           username=username)

@app.route('/graph')
def graph():
    return render_template('graph.html')


@app.route('/logout', methods=["POST"])
def logout():
    flash("Вы вышли из аккаунта!", 'info')
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
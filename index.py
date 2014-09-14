#! /usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import g
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://disciple:lolo@localhost:5432/disciplebase'


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    username = Column('name', String(15), unique=True)
    password = Column('password', String(50))
    email = Column('mail', String(50), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    """
    fonction ouvrantla page principale
    c'est la racine du site
    """
    return 'Hello'


def registered(login, password):
    result = False
    if login == 'test' and password == 'toto':
        result = True
    return result


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """
    page de creation d'un nouveau compte
    """
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'],
                request.form['mail'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    page de login
    """
    if request.method == 'GET':
        return render_template('login.html', titre='login')

    username = request.form['login']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,
                                           password=password).first()
    if registered_user is None:
        flash('Username or password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('profil'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profil/')
@login_required
def profil():
    return render_template('profil.html', titre='profil')


@app.route('/produits/')
def produits():
    return render_template('produits.html', titre='produit')


@app.route('/liste/')
@app.route('/liste/<id_liste>')
@login_required
def liste(id_liste=''):
    produits = ["sucre", "farine", "sel", "salade", "chou", "chocolat"]
    return render_template('liste.html', produits=produits, titre=id_liste)


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    app.run(debug=True)

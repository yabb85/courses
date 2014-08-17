#! /usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'
app.config['SQLALCHEMY_DATABASE_URL'] = \
    'postgresql://disciple:lolo@localhost:5432/disciplebase'


engine = create_engine('postgresql://disciple:lolo@localhost:5432/disciplebase',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    username = Column('name', String(15))
    password = Column('password', String(50))
    email = Column('mail', String(50))

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
    return 'Hello'


def registered(login, password):
    result = False
    if login == 'test' and password == 'toto':
        result = True
    return result


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'],
                request.form['mail'])
    db_session.add(user)
    db_session.commit()
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', titre='login')
    else:
        # username = request.form['login']
        # password = request.form['password']
        # registered_user = User.query.filter_by(username=username,
        # password=password).first()
        registered_user = User.query.all()
        if registered_user is None:
            return render_template('login.html', titre='login')
        login_user(registered_user)
        session['pseudo'] = request.form['login']
        return redirect(url_for('profil'))


@app.route('/logout/')
def logout():
    session.pop('pseudo', None)
    return redirect(url_for('login'))


@app.route('/profil/')
@login_required
def profil():
    return render_template('profil.html')


@app.route('/produits/')
def produits():
    return render_template('produits.html')


@app.route('/liste/')
@app.route('/liste/<id_liste>')
def liste(id_liste=''):
    produits = ["sucre", "farine", "sel", "salade", "chou", "chocolat"]
    return render_template('liste.html', produits=produits, titre=id_liste)


@app.context_processor
def transmit_data():
    dictionary = dict()
    if 'pseudo' in session:
        dictionary['pseudo'] = session['pseudo']
    return dictionary


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    db_session.commit()
    app.run(debug=True)

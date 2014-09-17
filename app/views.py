#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from app import db
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from flask import flash
from flask import g
from flask.ext.login import current_user
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from models import User
from models import UserList
from models import Liste
from models import Product


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
    """
    Logout de l'utilisateur
    detruit la session créé et redirige vers la page login
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/profil/')
@login_required
def profil():
    """
    Affiche la page de profil
    """
    return render_template('profil.html', titre='profil')


@app.route('/produits/')
def produits():
    return render_template('produits.html', titre='produit')


@app.route('/liste/')
@login_required
def list():
    """
    Affiche l'ensemble des liste de course de l'utilisateur
    """
    results = UserList.query.filter_by(user_id=g.user.id)
    listes = []
    for el in results:
        listes.append(Liste.query.filter_by(id=el.list_id).first())
    return render_template('liste.html', liste=listes)


@app.route('/liste/<id_liste>')
@login_required
def my_liste(id_liste=''):
    """
    Affiche la liste de course
    """
    name = Liste.query.filter_by(id=id_liste).first().name
    # produits = ["sucre", "farine", "sel", "salade", "chou", "chocolat"]
    produits = Product.query.all()
    return render_template('my_liste.html', produits=produits, titre=name,
                           id=id_liste)


@app.route('/addlist/', methods=['POST'])
def add_liste():
    liste = Liste(request.form['name'])
    db.session.add(liste)
    db.session.commit()
    list_user = UserList(g.user.id, liste.id)
    db.session.add(list_user)
    db.session.commit()
    return redirect('/liste/')


@app.route('/addproduct/', methods=['POST'])
def add_product():
    product = Product(request.form['name'], request.form['price'],
                      request.form['quantity'], request.form['unit'],
                      request.form['img'])
    db.session.add(product)
    db.session.commit()
    return redirect(request.args.get('next') or url_for('list'))


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

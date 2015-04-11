#! /usr/bin/python
# -*- coding:utf-8 -*-


"""
application Flask permettant de creer des listes de courses
"""

from app import app
from app import db
from app import api
from app.models import User
from flask import abort
from flask import jsonify
from flask import request
from flask import render_template
from flask_login import current_user
import json


@app.route('/')
def index():
    """
    Display the main page
    """
    return render_template('layout.html')


@app.route('/api/login/', methods=['POST'])
def login():
    """docstring for login"""
    user_to_login = json.loads(request.data)
    username = user_to_login.get("login")
    password = user_to_login.get("password")
    user = api.get_user(username, password)
    if user:
        return 'Success'
    else:
        return 'Fail'


@app.route('/api/logout/', methods=['POST', 'GET'])
def logout():
    """docstring for logout"""
    api.logout()
    return 'logout'


@app.route('/api/register/', methods=['POST'])
def register():
    """
    page de creation d'un nouveau compte
    """
    username = request.json.get('username')
    password = request.json.get('password')
    mail = request.json.get('mail')
    if not username or not password or not mail:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username, password, mail)
    db.session.add(user)
    db.session.commit()


@app.route('/api/connected/')
def connected():
    """docstring for connected"""
    return jsonify(connected=current_user.is_authenticated())


#@app.route('/profil/')
#@login_required
#def profil():
    #"""
    #Affiche la page de profil
    #"""
    #friends = search_friends(g.user.id)
    #return render_template('profil.html', titre='profil', friends=friends)



#@app.route('/addlist/', methods=['POST'])
#def add_liste():
    #"""
    #Creer une nouvelle liste pour l'utilisateur courant
    #"""
    #liste = Liste(request.form['name'])
    #db.session.add(liste)
    #db.session.commit()
    #list_user = UserList(g.user.id, liste.id)
    #db.session.add(list_user)
    #db.session.commit()
    #return redirect('/liste/')

#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'


@app.route('/')
def index():
    return 'Hello'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', titre='login')
    else:
        if request.form['login'] == 'test' and \
                request.form['password'] == 'toto':
            session['pseudo'] = request.form['login']
            return redirect(url_for('profil'))
        return render_template('login.html', titre='login')


@app.route('/profil/')
def profil():
    if 'pseudo' in session:
        return render_template('profil.html')
    return redirect(url_for('login'))


@app.route('/deconnexion/')
def deconnexion():
    session.pop('pseudo', None)
    return redirect(url_for('login'))


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


if __name__ == '__main__':
    app.run(debug=True)

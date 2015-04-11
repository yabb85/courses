#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
API to use course services
"""

from app import app
from app import db
from app.models import Friends
from app.models import Liste
from app.models import ListProduct
from app.models import Product
from app.models import User
from app.models import UserList
from flask import jsonify
from flask_login import current_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user


__login_manager__ = LoginManager()
__login_manager__.init_app(app)


def get_user(username, password):
    """Check if user exist"""
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return user
    else:
        return None


def logout():
    """docstring for logout"""
    logout_user()


@__login_manager__.user_loader
def load_user(user_id):
    """
    load user information
    """
    return User.query.get(int(user_id))


# move route #

@app.route('/api/list/')
@login_required
def api_all_list():
    """Return all list accessible by current user"""
    user_lists = db.session.query(UserList).filter(
        UserList.user_id == current_user.id)
    listes = []
    for element in user_lists:
        listes.append(db.session.query(Liste).filter(
            Liste.id == element.list_id).first().serialize)
    return jsonify(lists=listes)


@app.route('/api/list/<int:id_list>')
@login_required
def api_my_list(id_list=''):
    """Return the list identified by id_list"""
    list_prod = db.session.query(ListProduct).filter(
        ListProduct.list_id == id_list)
    return jsonify(achats=[i.serialize for i in list_prod.all()])


@app.route('/api/extended_list/<int:id_list>')
@login_required
def api_my_list_extended(id_list=''):
    """Return the list identified by id_list with all products use by list"""
    list_prod = db.session.query(ListProduct, Product).filter(
        ListProduct.list_id == id_list).join(Product, ListProduct.product_id ==
                                             Product.id)
    return jsonify(achats=[{'id': i[0].product_id, 'list': i[0].serialize,
                            'product': i[1].serialize}
                           for i in list_prod.all()])


@app.route('/api/products/')
@login_required
def api_products():
    """Return the list of products"""
    list_prod = db.session.query(Product).all()
    return jsonify(products=[prod.serialize for prod in list_prod])


@app.route('/api/products/<int:id_list>')
@login_required
def api_products_list_id(id_list=''):
    """Return the list of product used by list identified by id_list"""
    list_prod = db.session.query(ListProduct, Product).filter(
        ListProduct.list_id == id_list).join(Product, ListProduct.product_id ==
                                             Product.id)
    return jsonify(products=[i[1].serialize for i in list_prod.all()])


@app.route('/api/friends/')
@login_required
def api_friends():
    """Return a lsit of friend for current user"""
    results = db.session.query(Friends).filter(
        Friends.user_id == current_user.id)
    friends = []
    for user in results:
        friends.append(db.session.query(User).filter(
            User.id == user.friend).first())
    return jsonify(friends=[friend.serialize for friend in friends])

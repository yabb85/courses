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
from flask import g
from flask import jsonify
from flask_login import login_required


@app.route('/api/list/')
@login_required
def api_all_list():
    """docstring for api_all_list"""
    user_lists = db.session.query(UserList).filter(UserList.user_id==g.user.id)
    listes = []
    for element in user_lists:
        listes.append(db.session.query(Liste).filter(
            Liste.id == element.list_id).first().serialize)
    return jsonify(lists=listes)


@app.route('/api/list/<int:id_list>')
@login_required
def api_my_list(id_list=''):
    """docstring for api_my_list"""
    list_prod = db.session.query(ListProduct).filter(
        ListProduct.list_id==id_list)
    return jsonify(achats=[i.serialize for i in list_prod.all()])


@app.route('/api/extended_list/<int:id_list>')
@login_required
def api_my_list_extended(id_list=''):
    """docstring for api_my_list"""
    list_prod = db.session.query(ListProduct, Product).filter(
        ListProduct.list_id == id_list).join(Product, ListProduct.product_id ==
                                             Product.id)
    return jsonify(achats=[{'id': i[0].product_id, 'list': i[0].serialize,
                            'product': i[1].serialize}
                           for i in list_prod.all()])


@app.route('/api/products/')
@login_required
def api_products():
    """docstring for api_products"""
    list_prod = db.session.query(Product).all()
    return jsonify(products=[prod.serialize for prod in list_prod])


@app.route('/api/products/<int:id_list>')
@login_required
def api_products_list_id(id_list=''):
    """docstring for api_products"""
    list_prod = db.session.query(ListProduct, Product).filter(
        ListProduct.list_id == id_list).join(Product, ListProduct.product_id ==
                                             Product.id)
    return jsonify(products=[i[1].serialize for i in list_prod.all()])

@app.route('/api/friends/')
@login_required
def api_friends():
    """docstring for api_friends"""
    results = db.session.query(Friends).filter(Friends.user_id == g.user.id)
    friends = []
    for user in results:
        friends.append(db.session.query(User).filter(User.id==user.friend).first())
    return jsonify(friends=[friend.serialize for friend in friends])


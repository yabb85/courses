#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Wamp router
"""

from autobahn.twisted.wamp import Application
from app import db
from app.models import ListProduct
from app.models import Product
from app.models import UserList


wamp = Application('me.hory')


@wamp.signal('onjoined')
def _():
    """Executed during connection with client"""
    print 'session attached'


@wamp.register()
def add_to_list(product, liste):
    """Add a new product in liste on database"""
    result = ListProduct.query.filter_by(list_id=liste,
                                         product_id=product).first()
    number = 1
    if result is not None:
        # update le nombre de produit
        number = int(result.quantity) + 1
        result.quantity = number
    else:
        # ajoute un produit dans la liste
        lp = ListProduct(liste, product, number)
        db.session.add(lp)
    db.session.commit()
    prod = Product.query.filter_by(id=product).first()
    #wamp.session.publish('refresh_add_product', [product, liste, prod.name,
                                                 #prod.price, number, prod.unit,
                                                 #prod.img])
    wamp.session.publish('refresh_add_product', product, liste, prod.name,
                         number, prod.unit, prod.img)


@wamp.register()
def remove_to_list(product, liste):
    """remove a product in list on database"""
    ListProduct.query.filter_by(list_id=liste, product_id=product).delete()
    db.session.commit()
    wamp.session.publish('refresh_remove_product', product)


@wamp.register()
def create_product(name, price, quantity, unit, img):
    """Create a new product on database"""
    product = Product(name, price, quantity, unit, img)
    db.session.add(product)
    db.session.commit()
    wamp.session.publish('refresh_create_product', product.id, product.img,
                         product.name, product.quantity, product.unit)


@wamp.register()
def share_list(user_id, list_id):
    """Share a list with other user"""
    print "toto"
    list_user = UserList(user_id, list_id)
    db.session.add(list_user)
    db.session.commit()


if __name__ == '__main__':
    wamp.run(url='ws://127.0.0.1:8080/ws')

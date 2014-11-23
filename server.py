# -*- coding: utf-8 -*-

from autobahn.twisted.wamp import Application
from app import db
from app.models import ListProduct
from app.models import Product
from app.models import UserList


wamp = Application('me.hory')
wamp._data = {}


@wamp.signal('onjoined')
def _():
    print 'session attached'


@wamp.register()
def add_to_list(product, liste):
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
    wamp.session.publish('refresh_add_product', product, liste, prod.name,
                         prod.img, number)


@wamp.register()
def remove_to_list(product, liste):
    ListProduct.query.filter_by(list_id=liste, product_id=product).delete()
    db.session.commit()
    wamp.session.publish('refresh_remove_product', [product])


@wamp.register()
def create_product(name, price, quantity, unit, img):
    """docstring for create_product"""
    product = Product(name, price, quantity, unit, img)
    db.session.add(product)
    db.session.commit()
    wamp.session.publish('refresh_create_product', product.id, product.name)


@wamp.register()
def share_list(user_id, list_id):
    """docstring for share_list"""
    print "toto"
    list_user = UserList(user_id, list_id)
    db.session.add(list_user)
    db.session.commit()


if __name__ == '__main__':
    wamp.run(url='ws://127.0.0.1:5000/ws')

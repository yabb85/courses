# -*- coding: utf-8 -*-

from autobahn.twisted.wamp import Application
from app import db
from app.models import ListProduct
from app.models import Product


wamp = Application('me.hory')
wamp._data = {}


@wamp.signal('onjoined')
def _():
    print 'session attached'


@wamp.register()
def add_to_list(product, liste, name):
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
    wamp.session.publish('refresh_add_product', product, liste, name, prod.img,
                         number)


@wamp.register()
def remove_to_list(product, liste):
    ListProduct.query.filter_by(list_id=liste, product_id=product).delete()
    db.session.commit()
    wamp.session.publish('refresh_remove_product', [product])


@wamp.register()
def create_product(name, price, quantity, unit, img):
    """docstring for create_product"""
    product = Product(name, price, quantity, unit, img)
    print product
    db.session.add(product)
    db.session.commit()
    # travailler l'affichage dynamique lors d'un ajout

if __name__ == '__main__':
    wamp.run(url='ws://127.0.0.1:8080/ws')

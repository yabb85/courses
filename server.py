#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Wamp router
"""

from autobahn.twisted.wamp import ApplicationSession
from app import db
from app import config
from app.models import ListProduct
from app.models import Product
from app.models import UserList


class MyComponent(ApplicationSession):
    """docstring for MyComponent"""
    def onJoin(self, details):
        print 'session attached'

        def add_to_list(product, liste):
            """Add a new product in list on database"""
            result = ListProduct.query.filter_by(list_id=liste,
                                                product_id=product).first()
            number = 1
            if result is not None:
                # update le nombre de produit
                number = int(result.quantity) + 1
                result.quantity = number
            else:
                # ajoute un produit dans la liste
                new_prod = ListProduct(liste, product, number)
                db.session.add(new_prod)
            db.session.commit()
            prod = Product.query.filter_by(id=product).first()
            self.publish('refresh_add_product', product, liste, prod.name,
                                number, prod.unit, prod.img)
        self.register(add_to_list, 'me.hory.add_to_list');

        def remove_to_list(product, liste):
            """remove a product in list on database"""
            ListProduct.query.filter_by(list_id=liste, product_id=product).delete()
            db.session.commit()
            self.publish('refresh_remove_product', product)
        self.register(remove_to_list, 'me.hory.remove_to_list');

        def create_product(name, price, quantity, unit, img):
            """Create a new product on database"""
            product = Product(name, price, quantity, unit, img)
            db.session.add(product)
            db.session.commit()
            self.publish('refresh_create_product', product.id, product.img,
                                product.name, product.quantity, product.unit)
        self.register(create_product, 'me.hory.create_product');

        def share_list(user_id, list_id):
            """Share a list with other user"""
            list_user = UserList(user_id, list_id)
            db.session.add(list_user)
            db.session.commit()
        self.register(share_list, 'me.hory.share_list');

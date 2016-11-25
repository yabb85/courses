#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Define all routes used by api system
"""

from __future__ import print_function
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required
from flask_jwt import current_identity
from app.models import DATA_BASE
from app.models import Basket as db_Basket
from app.models import Product as db_Product
from app.security import create_user
from app.socketio import SOCKETIO


api = Api()


class Home(Resource):
    """
    Define List api
    """
    decorators = [jwt_required()]

    def __init__(self):
        super(Home, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='')

    def get(self):
        """
        Display list of baskets possessed by user
        """
        baskets = []
        for element in current_identity.baskets:
            baskets.append({
                'id': element.id,
                'name': element.name
            })
        return {
            'Baskets': baskets
        }

    def post(self):
        """
        Create new basket for current user
        """
        args = self.parser.parse_args()
        name = args['name']
        basket = db_Basket(name=name, description="")
        basket.users.append(current_identity)
        DATA_BASE.session.add(basket)
        DATA_BASE.session.commit()
        DATA_BASE.session.refresh(current_identity)
        baskets = []
        for element in current_identity.baskets:
            baskets.append({
                'id': element.id,
                'name': element.name
            })
        return {
            'Baskets': baskets
        }


class Basket(Resource):
    """
    Define list of Basket
    """
    decorators = [jwt_required()]

    def __init__(self):
        """docstring for __init__"""
        super(Basket, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')

    def get(self, basket_id):
        """
        Return description of list with products in basket
        """
        basket = db_Basket.query.get(basket_id)
        products = []
        for element in basket.orders:
            print(element.__dict__)
            product_id = element.products_id
            product = db_Product.query.get(product_id)
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': element.quantity
            })
        return {
            'id': basket_id,
            'name': basket.name,
            'inBasket': products
        }

    def post(self, basket_id):
        """
        Add new product to selected basket
        """
        args = self.parser.parse_args()
        basket = db_Basket.query.get(basket_id)
        product = db_Product.query.get(args['id'])
        founded = False
        for element in basket.orders:
            if product.id == element.products_id:
                element.quantity += 1
                founded = True
        if not founded:
                basket.add_product(product, 1)
        DATA_BASE.session.commit()
        products = []
        for element in basket.orders:
            product_id = element.products_id
            product = db_Product.query.get(product_id)
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': element.quantity
            })
        data = {
            'id': basket_id,
            'name': basket.name,
            'inBasket': products
        }
        SOCKETIO.emit('update', data, room=basket_id)
        return data

    def delete(self, basket_id):
        """
        Remove a product of selected basket
        """
        args = self.parser.parse_args()
        basket = db_Basket.query.get(basket_id)
        product = db_Product.query.get(args['id'])
        basket.remove_product(product)
        DATA_BASE.session.commit()
        products = []
        for element in basket.orders:
            product_id = element.products_id
            product = db_Product.query.get(product_id)
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': element.quantity
            })
        data = {
            'id': basket_id,
            'name': basket.name,
            'inBasket': products
        }
        SOCKETIO.emit('update', data, room=basket_id)
        return data



class User(Resource):
    """Manage User"""
    def __init__(self):
        super(User, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='')
        self.parser.add_argument('password', type=str, help='')
        self.parser.add_argument('email', type=str, help='')

    def post(self):
        """docstring for psott"""
        args = self.parser.parse_args()
        name = args['name']
        password = args['password']
        email = args['email']
        return create_user(name, password, email)


class Product(Resource):
    """
    Manage products
    """
    decorators = [jwt_required()]

    def __init__(self):
        """docstring for __init__"""
        super(Product, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='')
        self.parser.add_argument('img', type=str, help='')

    def get(self):
        """docstring for get"""
        products = db_Product.query.filter()
        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name': product.name,
                'img': product.img
            })
        return {
            'products': result
        }

    def post(self):
        """
        Create new product
        """
        args = self.parser.parse_args()
        name = args['name']
        img = args['img']
        product = db_Product(name, img)
        DATA_BASE.session.add(product)
        DATA_BASE.session.commit()
        products = db_Product.query.all()
        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name': product.name,
                'img': product.img
            })
        return {
            'products': result
        }


api.add_resource(Home, '/api/baskets')
api.add_resource(Basket, '/api/baskets/<string:basket_id>')
api.add_resource(User, '/api/users')
api.add_resource(Product, '/api/products')

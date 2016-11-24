#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Define all models used by API
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import uuid


DATA_BASE = SQLAlchemy()


# Define Models

ROLES_USERS = Table('roles_users', DATA_BASE.metadata,
                    Column('users_id', Integer(), ForeignKey('users.id')),
                    Column('roles_id', Integer(), ForeignKey('roles.id')))


BASKETS_USERS = Table('baskets_users', DATA_BASE.metadata,
                      Column('users_id', Integer(), ForeignKey('users.id')),
                      Column('baskets_id', Integer(), ForeignKey('baskets.id')))


class User(DATA_BASE.Model):
    """define Users storage format"""
    __tablename__ = 'users'
    id = Column(String(35), primary_key=True, unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean)
    username = Column(String(15), unique=True)
    roles = relationship('Role', secondary=ROLES_USERS,
                         backref=backref('users', lazy='dynamic'))
    baskets = relationship('Basket', secondary=BASKETS_USERS,
                           backref=backref('users', lazy='dynamic'))

    def __init__(self, name, password, email):
        """Create new user in database"""
        DATA_BASE.Model.__init__(self)
        self.id = uuid.uuid4().hex
        self.username = name
        self.password = password
        self.email = email

    def set_password(self, password):
        """Hash password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password, password)


class Role(DATA_BASE.Model):
    """Define roles storage format"""
    __tablename__ = 'roles'
    id = Column(String(35), primary_key=True, unique=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __init__(self, name=None, description=None):
        DATA_BASE.Model.__init__(self)
        self.id = uuid.uuid4().hex
        self.name = name
        self.description = description


class Order(DATA_BASE.Model):
    """
    List of ordered products
    """
    __tablename__ = 'orders'
    id = Column(String(35), primary_key=True, unique=True)
    baskets_id = Column(Integer(), ForeignKey('baskets.id'), primary_key=True)
    products_id = Column(Integer(), ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer())

    basket = relationship('Basket',
                          backref=backref('orders',
                                          cascade="all, delete-orphan"))
    product = relationship('Product',
                           backref=backref('orders',
                                           cascade="all, delete-orphan"))

    def __init__(self, basket=None, product=None, quantity=None):
        DATA_BASE.Model.__init__(self)
        self.id = uuid.uuid4().hex
        self.basket = basket
        self.product = product
        self.quantity = quantity

    def __repr__(self):
        return '<Order {}>'.format(self.basket.name + " " + self.product.name)


class Basket(DATA_BASE.Model):
    """
    List of basket with description
    """
    __tablename__ = "baskets"
    id = Column(String(35), primary_key=True, unique=True)
    name = Column(String(50))
    description = Column(String(255))

    products = relationship("Product", secondary="orders", viewonly=True)

    def __init__(self, name, description):
        """Initialize a new Basket"""
        DATA_BASE.Model.__init__(self)
        self.id = uuid.uuid4().hex
        self.name = name
        self.description = description

    def add_product(self, prod, qty):
        """Add new product in basket"""
        self.orders.append(Order(basket=self, product=prod, quantity=qty))

    def remove_product(self, prod):
        """Remove a product of basket"""
        order = Order.query.filter_by(baskets_id=self.id, products_id=prod.id).first()
        self.orders.remove(order)

    def __repr__(self):
        return '<Order {}>'.format(self.name)


class Product(DATA_BASE.Model):
    """
    Products used by user
    """
    __tablename__ = "products"
    id = Column(String(35), primary_key=True, unique=True)
    name = Column(String(50))
    img = Column(String(200))

    baskets = relationship("Basket", secondary="orders", viewonly=True)

    def __init__(self, name, img):
        """
        Initialize a new product
        """
        DATA_BASE.Model.__init__(self)
        self.id = uuid.uuid4().hex
        self.name = name
        self.img = img

    def __repr__(self):
        return '<Product {}>'.format(self.name)

#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    username = Column('name', String(15), unique=True)
    password = Column('password', String(50))
    email = Column('mail', String(50), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Liste(db.Model):
    __tablename__ = "list"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))

    def __init__(self, name):
        """docstring for __init__"""
        self.name = name

    def __repr__(self):
        """docstring for __repr__"""
        return '<Liste %r>' % self.name


class UserList(db.Model):
    __tablename__ = 'user_list'
    user_id = Column('user_id', Integer, primary_key=True)
    list_id = Column('list_id', Integer, primary_key=True)

    def __init__(self, user_id, list_id):
        """docstring for __init__"""
        self.user_id = user_id
        self.list_id = list_id

    def __repr__(self):
        """docstring for __repr__"""
        return '<User List %r %r>' % (self.user_id, self.list_id)


class Product(db.Model):
    __tablename__ = "products"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    price = Column('price', Numeric)
    quantity = Column('quantity', Integer)
    unit = Column('unit', String(10))
    img = Column('img', String(200))

    def __init__(self, name, price, quantity, unit, img):
        """docstring for __init__"""
        self.name = name
        self.price = price
        self.quantity = quantity
        self.unit = unit
        self.img = img

    def __repr__(self):
        return '<Product %r %r %r>' % (self.id, self.name, self.price)


class ListProduct(db.Model):
    __tablename__ = "list_product"
    list_id = Column('list_id', Integer, primary_key=True)
    product_id = Column('product_id', Integer, primary_key=True)
    quantity = Column('quantity', Integer)

    def __init__(self, list_id, product_id, quantity):
        """docstring for __init__"""
        self.list_id = list_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        """docstring for __repr__"""
        return '<ListProduct %r %r %r>' % (self.list_id, self.product_id,
                                           self.quantity)


class Friends(db.Model):
    __tablename__ = "friends"
    user_id = Column('user_id', Integer, primary_key=True)
    friend = Column('friend', Integer, primary_key=True)

    def __init__(self, user_id, friend):
        self.user_id = user_id
        self.friend = friend

    def __repr__(self):
        """docstring for __repr__"""
        return '<Friend %r %r>' % (self.user_id, self.friend)

#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, String
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

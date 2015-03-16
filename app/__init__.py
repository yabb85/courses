#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
Initialisation package
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_triangle import Triangle


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://disciple:lolo@localhost:5432/disciplebase'
Triangle(app)
db = SQLAlchemy(app)

from app import views, models, api

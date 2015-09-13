#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
Initialisation package
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_triangle import Triangle
from ConfigParser import ConfigParser


config = ConfigParser(os.environ)
config.read('../config/config.txt')


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://' + config.get('bdd', 'user') + ':' + \
    config.get('bdd', 'pass') + '@' + config.get('bdd', 'url') + \
    ':' + config.get('bdd', 'port') + '/' + config.get('bdd', 'base')

Triangle(app)
db = SQLAlchemy(app)

from app import views, models, api

#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'gjbd iud,hghb nux, b'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://disciple:lolo@localhost:5432/disciplebase'
db = SQLAlchemy(app)

from app import views, models

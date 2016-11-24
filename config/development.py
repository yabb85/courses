#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Define development configuration
"""

from datetime import timedelta

DEBUG = True
SECRET_KEY = 'Development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
JWT_EXPIRATION_DELTA = timedelta(seconds=36000000)

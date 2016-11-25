#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Define default configuration
"""

from datetime import timedelta

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@localhost:5432/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_AUTH_URL_RULE = '/api/login'
JWT_AUTH_USERNAME_KEY = 'login'
JWT_EXPIRATION_DELTA = timedelta(seconds=3600)

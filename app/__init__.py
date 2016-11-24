#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Initialisation package
"""
import os
from flask import Flask
from flask_restful import Api
from app.models import DATA_BASE
from app.api import api
from app.security import security
from app.views import simple_page
from app.socketio import socketio


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')
app.register_blueprint(simple_page)
DATA_BASE.init_app(app)
api.init_app(app)
security.init_app(app)
socketio.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Initialize the database"""
    DATA_BASE.create_all()
    print "database initialized"

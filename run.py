#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from app.socketio import SOCKETIO

if __name__ == '__main__':
    SOCKETIO.run(app)
    # app.run()

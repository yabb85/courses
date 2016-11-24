#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from app.socketio import socketio

if __name__ == '__main__':
    socketio.run(app)
    # app.run()

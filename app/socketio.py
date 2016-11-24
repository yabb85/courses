#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Create socketio server
"""

from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

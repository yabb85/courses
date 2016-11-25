#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Create socketio server
"""

from flask_socketio import SocketIO
from flask_socketio import join_room
from flask_socketio import leave_room

SOCKETIO = SocketIO()


@SOCKETIO.on('join')
def on_join(data):
    """docstring for on_join"""
    room = data['room']
    join_room(room)

@SOCKETIO.on('leave')
def on_leave(data):
    """docstring for on_leave"""
    room = data['room']
    leave_room(room)

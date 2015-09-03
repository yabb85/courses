#! /usr/bin/python
# -*- coding:utf-8 -*-


"""
application Flask permettant de creer des listes de courses
"""

from app import app
from app import api
from app.models import User
from flask import abort
from flask import jsonify
from flask import request
from flask import render_template
from flask_login import current_user
from flask_login import login_required
import json


@app.route('/')
def index():
    """
    Display the main page
    """
    return render_template('layout.html')


# login and logout

@app.route('/api/login/', methods=['POST'])
def login():
    """Login the current user."""
    user_to_login = json.loads(request.data)
    username = user_to_login.get("login")
    password = user_to_login.get("password")
    user = api.get_user(username, password)
    if user:
        return 'Success'
    else:
        abort(401)


@app.route('/api/logout/', methods=['POST'])
def logout():
    """Logout the current user."""
    api.logout()
    return 'logout'


@app.route('/api/register/', methods=['POST'])
def register():
    """
    page de creation d'un nouveau compte
    Create a new user
    """
    user_to_create = json.loads(request.data)
    username = user_to_create.get('name')
    mail = user_to_create.get('mail')
    password = user_to_create.get('password')
    if not username or not password or not mail:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    return api.add_user(username, password, mail)


@app.route('/api/connected/', methods=['GET'])
def connected():
    """Return if current user is logged"""
    return jsonify(connected=current_user.is_authenticated())


# list of Carts

@app.route('/api/list/', methods=['POST'])
@login_required
def create_new_list():
    """Create a new liste for current user."""
    cart_to_create = json.loads(request.data)
    cart_name = cart_to_create.get('name')
    return api.create_new_list(current_user.id, cart_name)


@app.route('/api/list/<int:list_id>', methods=['DELETE'])
@login_required
def remove_list(list_id=''):
    """remove a list defined by list_id"""
    try:
        api.remove_list(list_id)
    except:
        return 'Fail'
    return 'Success'


@app.route('/api/share/', methods=['POST'])
@login_required
def share():
    """docstring for share_user"""
    data = json.loads(request.data)
    friend = data.get('friend')
    cart = data.get('cart')
    return api.share_list(friend, cart)


# profil

@app.route('/api/friend/', methods=['POST'])
@login_required
def add_friend():
    """docstring for add_friend"""
    friend = json.loads(request.data)
    friend_name = friend.get('name')
    friend_mail = friend.get('mail')
    if not friend_mail and not friend_name:
        return 'Fail'
    friend_id = api.search_user(friend_name)
    if friend_id:
        api.add_friend(friend_id)
    else:
        api.send_mail(friend_mail)
    return 'Success'

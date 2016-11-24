#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Define security interface for website
Manage login with '/api/login'
generate jwt token
"""

from app.models import DATA_BASE
from app.models import User
from flask_jwt import JWT
from flask_jwt import JWTError
from flask import current_app
from flask import request
from datetime import datetime
from werkzeug.security import safe_str_cmp
from sqlalchemy import or_


security = JWT()


@security.authentication_handler
def authenticate_handler(login, password):
    """
    Mange authentication user
    """
    user = get_user(login, password)
    if user:
        return user


@security.identity_handler
def identity_handler(payload):
    """
    Verify token for current request
    """
    user_id = payload['identity']
    return load_user(user_id)


@security.jwt_payload_handler
def payload_handler(identity):
    """
    Define information in payload of token
    """
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    username = getattr(identity, 'username') or identity['username']
    identity = getattr(identity, 'id') or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity,
            'username': username}


@security.auth_request_handler
def auth_request_handler():
    """
    Retrieve parameter of POST login request and generate token
    """
    data = request.get_json()
    if not data:
        raise JWTError('Bad Request', 'Invalid credentials')

    username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    password = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
    criterion = [username, password, len(data) == 2]

    if not all(criterion):
        raise JWTError('Bad Request', 'Invalid credentials')

    identity = security.authentication_callback(username, password)

    if identity:
        access_token = security.jwt_encode_callback(identity)
        return security.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials')


def get_user(mail_or_username, password):
    """
    Check user and return user if exist
    """
    user = User.query.filter(or_(User.email == mail_or_username,
                                 User.username == mail_or_username)).first()
    if user and safe_str_cmp(user.password.encode('utf-8'),
                             password.encode('utf-8')):
        return user


def load_user(user_id):
    """docstring for load_user"""
    return User.query.get(user_id)


def create_user(name, password, email):
    user = User(name, password, email)
    try:
        DATA_BASE.session.add(user)
        DATA_BASE.session.commit()
    except Exception as e:
        print e
        return {'message': 'this user already exist'}
    return {'message': 'new user created'}
    # access_token = security.jwt_encode_callback(user)
    # return security.auth_response_callback(access_token, user)

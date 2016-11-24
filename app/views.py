#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template


simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/', defaults={'path': ''})
@simple_page.route('/<path:path>')
def index(path):
    """
    Display the main page
    """
    return render_template('layout.html')

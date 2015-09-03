#! /usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from app import config

if __name__ == '__main__':
    app.run(host=config.get('flask', 'url'),
            port=config.getint('flask', 'port'),
            debug=True)

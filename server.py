# -*- coding: utf-8 -*-

from autobahn.twisted.wamp import Application


app = Application('com.example')
app._data = {}


@app.signal('onjoined')
def _():
    print 'session attached'


if __name__ == '__main__':
    app.run(url='ws://127.0.0.1:8080/ws')

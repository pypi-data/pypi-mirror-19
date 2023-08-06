#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import flask

RESPONSE_CODE = 200

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def hello(path):
    global RESPONSE_CODE
    if RESPONSE_CODE == 200:
        return 'Hi!\n'
    else:
        flask.abort(RESPONSE_CODE)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind-address',
                        dest='bind', default='127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', default=4000, type=int)
    parser.add_argument('-c', '--response_code', dest='code', default=200, type=int)
    return parser.parse_args()

def main():
    global RESPONSE_CODE
    opts = parse_args()
    RESPONSE_CODE = opts.code
    app.run(host=opts.bind, port=opts.port)

if __name__ == "__main__":
    main()

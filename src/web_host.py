#!/usr/bin/env python
#coding: utf8

import json

from gevent import monkey, pool, sleep
monkey.patch_all()

# https://gist.github.com/werediver/4358735
from bottle import get, post, request, response
from bottle import GeventServer, run

from main import query_master_server, query_server

addr_gen = query_master_server()

@get('/')
def index():
    return open('index.html', 'r').read()

@get('/enum_server')
def enum_server():
    response.content_type  = 'text/event-stream'
    response.cache_control = 'no-cache'
    yield 'retry: 1000\n\n'
    r = addr_gen.next()
    print r
    if r:
        yield 'data: %s' % json.dumps(query_server(r))
 
if '__main__' == __name__:
    run(server=GeventServer)

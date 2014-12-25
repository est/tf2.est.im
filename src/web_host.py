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
    yield 'retry: 1000\n'
    tasks = pool.Pool(50)
    for r in tasks.imap_unordered(query_server, query_master_server()):
        if r:
            yield 'data: %s\n\n' % json.dumps(r)
 
if '__main__' == __name__:
    run(server=GeventServer)

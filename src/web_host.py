#!/usr/bin/env python
#coding: utf8

import socket
import tornado.ioloop
import tornado.web

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class IPList(object):
    def __init__(self):
        # master server
        # "https://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol"
        self.ms_conn = s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ms_conn.settimeout(5)
        self.last_addr = ('0.0.0.0', 0)

    def 

if __name__ == "__main__":
    tornado.web.Application([
        (r"/", WebHandler),
    ]).listen(8888)
    tornado.ioloop.IOLoop.instance().start()

#!/usr/bin/env python
# coding: utf8
import time

from gevent import monkey, spawn, sleep, socket
monkey.patch_all()

import valve.source.master_server
import valve.source.a2s

class GBaseServer(object): #valve.source.a2s.BaseServerQuerier):

    def __init__(self, address, timeout=5.0):
        self.host = address[0]
        self.port = address[1]
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)

    def request(self, request):
        self.socket.sendto(request.encode(), (self.host, self.port))

    def get_response(self):
        return self.socket.recv(1400)

class GMasterServer(GBaseServer, valve.source.master_server.MasterServerQuerier):
    
    def __init__(self, address=valve.source.master_server.MASTER_SERVER_ADDR, timeout=10.0):
        super(GMasterServer, self).__init__(address, timeout)


class GServerQuerier(GBaseServer, valve.source.a2s.ServerQuerier):
    pass

def get_all():
    msq = GMasterServer()
    for address in msq.find(region=u'all',
                        gamedir="tf",
                        map="ctf_2fort"):
        
        server = GServerQuerier(address)
        t1 = time.time()
        info = server.get_info()
        ttl = time.time() - t1
        if not info['password_protected']:
            print  '%s:%s\t%03dms\t%s\t%s\t%s/%s' % (
                address[0], 
                address[1], 
                ttl * 1000,
                info['server_name'][:15], 
                info['map'], 
                info['player_count'], info['max_players']
            )





if '__main__' == __name__:
    
    import readline, rlcompleter; readline.parse_and_bind("tab: complete")


    __import__('BaseHTTPServer').BaseHTTPRequestHandler.address_string = lambda x:x.client_address[0]
    # run(application, host='0.0.0.0', port=8002, reload=True)

    get_all()

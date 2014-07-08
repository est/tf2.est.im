#!/usr/bin/env python
# coding: utf8
import time

from gevent import monkey, spawn, sleep
monkey.patch_all()

import valve.source.master_server
import valve.source.a2s

def get_all():
    msq = valve.source.master_server.MasterServerQuerier()
    for address in msq.find(region=u'all',
                        gamedir="tf",
                        map="ctf_2fort"):
        
        server = valve.source.a2s.ServerQuerier(address)
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

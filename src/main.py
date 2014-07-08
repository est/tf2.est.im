#!/usr/bin/env python
# coding: utf8

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
        info = server.get_info()
        fields = ['server_name', 'map', 'player_count', 'max_players', 'bot_count', 'password_protected']
        print  address, '\t'.join(info[f] for f in fields)





if '__main__' == __name__:
    
    import readline, rlcompleter; readline.parse_and_bind("tab: complete")


    __import__('BaseHTTPServer').BaseHTTPRequestHandler.address_string = lambda x:x.client_address[0]
    # run(application, host='0.0.0.0', port=8002, reload=True)

    get_all()

#!/usr/bin/env python
# coding: utf8
import time, struct

from gevent import monkey, spawn, sleep, socket
monkey.patch_all()


S0 = "hl2master.steampowered.com:27011"
S1 = "208.64.200.52:27011"
S2 = "208.64.200.39:27011"

def query_master_server(master_addr=("208.64.200.52", 27011)):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    last_addr = ('0.0.0.0', 0)
    while 1:
        s.sendto('1\xFF%s:%s\0\\gamedir\\tf\0' % (last_addr[0], last_addr[1]), master_addr)
        b = s.recv(1400)
        if b.startswith('\xFF\xFF\xFF\xFF\x66\x0A'):
            i = 6
        else:
            i = 0
        while i<len(b):
            saddr = b[i:i+6]
            this_addr = socket.inet_ntoa(b[i:i+4]), struct.unpack('!H', b[i+4:i+6])[0]
            if this_addr != last_addr:
                last_addr = this_addr
                yield last_addr
            i += 6
        print 'next packet'
        # break





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
    
    # import readline, rlcompleter; readline.parse_and_bind("tab: complete")


    # __import__('BaseHTTPServer').BaseHTTPRequestHandler.address_string = lambda x:x.client_address[0]
    # run(application, host='0.0.0.0', port=8002, reload=True)

    for a in query_master_server():
        print a

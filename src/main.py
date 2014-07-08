#!/usr/bin/env python

# coding: utf8

import valve.source.master_server

def get_all():
    msq = valve.source.master_server.MasterServerQuerier()
    for address in msq.find(region=u'all',
                        gamedir="tf",
                        map="ctf_2fort"):
        print "{0}:{1}".format(*address)





if '__main__' == __name__:
    
    import readline, rlcompleter; readline.parse_and_bind("tab: complete")


    __import__('BaseHTTPServer').BaseHTTPRequestHandler.address_string = lambda x:x.client_address[0]
    # run(application, host='0.0.0.0', port=8002, reload=True)

    get_all()

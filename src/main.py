#!/usr/bin/env python

# coding: utf8

import valve.source.master_server

def get_all():
	pass




if '__main__' == __name__:
    
    import readline, rlcompleter; readline.parse_and_bind("tab: complete")


    __import__('BaseHTTPServer').BaseHTTPRequestHandler.address_string = lambda x:x.client_address[0]
    # run(application, host='0.0.0.0', port=8002, reload=True)

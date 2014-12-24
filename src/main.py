#!/usr/bin/env python
# coding: utf8
import time, struct
import locale

from gevent import monkey, spawn, sleep, socket, pool
monkey.patch_all()

ENCODING = locale.getdefaultlocale()[1]

S0 = "hl2master.steampowered.com:27011"
S1 = "208.64.200.52:27011"
S2 = "208.64.200.39:27011"

result = open('result.txt', 'w')

def query_master_server(master_addr=("208.64.200.52", 27011)):
    "https://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    prev_addr = ('0.0.0.0', 0)
    first_addr = None
    list_has_more = True
    while list_has_more:
        s.sendto('1\xFF%s:%s\0\\gamedir\\tf\0' % (prev_addr[0], prev_addr[1]), master_addr)
        try:
            b = s.recv(1400)
        except socket.timeout as err:
            continue
        if b.startswith('\xFF\xFF\xFF\xFF\x66\x0A'):
            i = 6
        else:
            i = 0
        while i<len(b):
            saddr = b[i:i+6]
            this_addr = socket.inet_ntoa(b[i:i+4]), struct.unpack('!H', b[i+4:i+6])[0]

            if first_addr == this_addr:
                # print first_addr, this_addr
                list_has_more = False
                break
            elif first_addr is None:
                first_addr = this_addr

            if this_addr != prev_addr:
                prev_addr = this_addr
                yield prev_addr
            i += 6
        # print 'next packet'
        # break

def mute_exception(func):
    def wrapper(*args,  **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return
    return wrapper



@mute_exception
def query_server(svr_addr):
    timeout_retries = 3
    t0 = 0
    data = None
    while timeout_retries>0:
        t0 = time.time()
        "https://developer.valvesoftware.com/wiki/Server_queries"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto('\xFF\xFF\xFF\xFF\x54Source Engine Query\0', svr_addr)
        try:
            data = s.recv(1400)
            break
        except socket.timeout:
            timeout_retries -= 1
            continue
    if not data: return
    out = {'rtt': time.time() - t0 }
    fields = data[6:].split('\0') # 4 byte header, "I", version
    out.update((k, fields[i]) for i, k in enumerate(
        'server_name map_name folder_name game_name'.split(' ')
    ))
    remains = struct.unpack('<HBBBBBBB', '\0'.join(fields[4:])[:9])
    out.update((k, remains[i]) for i, k in enumerate([
        'game_steam_id', 'players_no', 'max_players', 'bots_no', 
        'server_type', 'server_os', 'has_password', 'has_vac' 
    ]))
    return out

def get_server_desc(svr_addr):
    ret = query_server(svr_addr)
    if not ret: return
    if ret['map_name'].startswith((
        'ach',
        'vsh_',
        'cp_orange_',
        'trade_',
        'ctf_2fort',
    )) or ret['players_no']==0 or ret['rtt']>0.4:
        return
    fmt = '%15s:%-5s %3sms %-24s %2d/%-2d %-2s %s'
    params = (
        svr_addr[0], svr_addr[1], 
        int(ret['rtt'] * 1000),
        ret['map_name'][:24],
        ret['players_no'], ret['max_players'], 
        ret['bots_no'] if ret['bots_no'] else '',
    )
    result.write(fmt % (params + (ret['server_name'],)))
    result.write('\n')
    sn = ret['server_name'][:17].decode('utf8', 'ignore').encode(ENCODING, 'ignore')
    print  fmt % (params + (sn.strip(),))

def get_all():
    msq = valve.source.master_server.MasterServerQuerier()
    for address in msq.find(region=u'all',
                        gamedir="tf",
                        map="ctf_2fort"):
        
        server = valve.source.a2s.ServerQuerier(address)
        t1 = time.time()
        info = server.get_info()
        ttl = time.time() - t1
        if not info['password_protected'] and ttl<0.300:
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


    p = pool.Pool(100)
    p.map(get_server_desc, query_master_server())
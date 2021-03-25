import socket
import struct
import sys
import threading

def main(dest_name):
    try:
        dest_addr = socket.gethostbyname(dest_name)
    except socket.error as e:
        print('==== Error: %d, %s' % (e.errno, e.strerror))
        sys.exit()
    dest_port = 65432
    max_hops = 30
    ttl = 1
    is_dest = False
    while True:
        current_addr = None
        current_name = None
        current_host = None
#Todo
#finish typing the code
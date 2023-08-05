#!/usr/bin/python
from __future__ import print_function
import sys
import time
import argparse
import threading
import functools


if sys.version_info[0] == 2:
    import SocketServer
else:
    import socketserver as SocketServer
    ord = lambda b: b


BUF_SIZE = 8192
DEFAULT = {
    'host': '127.0.0.1',
    'port': 9000,
    'limit': 40,
}


def pp(fmt, *args, **kwargs):
    if kwargs.get('fire'):
        msg = fmt.format(*args, data=format_bytes(**kwargs))
        print(msg)


def format_bytes(data, mode=None, limit=None, **kwargs):
    if mode == 'hex':
        data = map(lambda b: format(ord(b), '02x'), data)
    else:
        data = map(ord, data)
    data = list(data)

    if limit is not None and len(data) > limit:
        return '{} ... ({}/{})'.format(data[:limit], limit, len(data))
    else:
        return '{}'.format(data)


class TcpEchoHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data) == 0:
                break
            pp('{data}', data=data)
            self.request.sendall(data)


class UdpEchoHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        conn = self.request[1]
        pp('{}:{} =>\n    {data}',
           self.client_address[0],
           self.client_address[1],
           data=data)
        conn.sendto(data, self.client_address)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


def start_tcp_server(addr):
    SocketServer.TCPServer.allow_reuse_address = True
    s = ThreadedTCPServer(addr, TcpEchoHandler)
    s.serve_forever()


def start_udp_server(addr):
    SocketServer.UDPServer.allow_reuse_address = True
    s = ThreadedUDPServer(addr, UdpEchoHandler)
    s.allow_reuse_address = True
    s.serve_forever()


def run_servers(args):
    addr = (args['host'], args['port'])
    print("start echo server on {}:{}...".format(*addr))
    threads = [
        threading.Thread(target=start_tcp_server, args=(addr,)),
        threading.Thread(target=start_udp_server, args=(addr,)),
    ]

    for t in threads:
        t.setDaemon(True)
        t.start()
    while threading.active_count() > 0:
        time.sleep(1)


def main():
    desc = '''A simple TCP/UDP echo server.'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--host', default=DEFAULT['host'],
                        help='server address [default: {}]'
                        .format(DEFAULT['host']))
    parser.add_argument('--port', type=int, default=DEFAULT['port'],
                        help='server port [default: {}]'
                        .format(DEFAULT['port']))
    parser.add_argument('--print', action='store_true',
                        help='print out what received')
    parser.add_argument('--limit', type=int, default=DEFAULT['limit'],
                        help='print out how many bytes [default: {}]'
                        .format(DEFAULT['limit']))
    parser.add_argument('--hex', action='store_true',
                        help='print bytes with hex format')
    args = vars(parser.parse_args())

    if args['print']:
        mode = 'hex' if args['hex'] else None
        limit = args['limit']
        global pp
        pp = functools.partial(pp, fire=True, mode=mode, limit=limit)
    try:
        run_servers(args)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
'''
Created on 2016-12-24

@author: hustcc
'''

import click
try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except:
    from http.server import SimpleHTTPRequestHandler, HTTPServer


__version__ = '0.0.1'


@click.command()
@click.argument('port', type=click.INT, default=8000)
@click.option('--host', default='127.0.0.1',
              help='The binding host of server.')
def server(port, host):
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass = HTTPServer
    Protocol = "HTTP/1.0"
    server_address = (host, port)
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print ("Serving HTTP on %s:%s..." % (sa[0], sa[1]))
    httpd.serve_forever()


def run():
    server()


if __name__ == '__main__':
    run()

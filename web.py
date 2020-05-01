#!/usr/bin/python
# -*- coding: utf-8 -*-
import http.server as BaseHTTPServer
import http.server as CGIHTTPServer
                                   
def web():
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("", 8008)
    handler.cgi_directories = ["/cgi"]

    httpd = server(server_address, handler)
    httpd.serve_forever()

if __name__ == '__main__':
    web()

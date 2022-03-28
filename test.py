#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        self.message = xy
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write(bytes(self.message, "utf8"))
        return
    def run():
        print('Avvio del server...')
        server_address = ('0.0.0.0', 8080)
        httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
        print('Server in esecuzione...')
        httpd.serve_forever()




with open("html/index.html",'r') as f:
    xy = ""
    print ("Aperto")
    line = f.readline()
    while line:
        xy = xy + line.strip()
        line = f.readline()
        print (xy)

HTTPServer_RequestHandler.run()
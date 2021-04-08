from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = 'localhost'
serverPort = 8080
class S(BaseHTTPRequestHandler):
    def _send_respheader(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._send_respheader()
        self.wfile.write(bytes('<html><head><title>https://iAIClab.tku.edu.tw</title></head>', 'utf-8'))
        self.wfile.write(bytes('<p>Request: %s</p>' % self.path, 'utf-8'))
        self.wfile.write(bytes('<body>', 'utf-8'))
        self.wfile.write(bytes('<p>This web page is the result of HTTP get message.</p>', 'utf-8'))
        self.wfile.write(bytes('</body></html>', 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print('POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n',
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._send_respheader()
        self.wfile.write('POST request for {}'.format(self.path).encode('utf-8'))

def main(server_class=HTTPServer, handler_class=S):
    print('Starting httpd server..%s:%d\n' % (hostName, serverPort))
    server_address = ('', serverPort)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stoping https server..\n')

if __name__ == '__main__':
    main()

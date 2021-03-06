from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

hostName = 'localhost'
serverPort = 8080
class B(BaseHTTPRequestHandler):
    def _send_respheader(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._send_respheader()
        name = 'world'
        query_components = parse_qs(urlparse(self.path).query)
        if 'name' in query_components:
            name = query_components['name'][0]

        f_index = open('index.html', 'r')
        html_ori = f_index.read()
        html_split = html_ori.split('</body>', 1)
        html = html_split[0]
        html += '<h2>Hello ' + str(name) + ' !</h2></body></html>'
        self.wfile.write(bytes(html, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print('POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n',
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._send_respheader()
        self.wfile.write('POST request for {}'.format(self.path).encode('utf-8'))

    def do_HEAD(self):
        self._send_respheader()

def main(server_class=HTTPServer, handler_class=B): #handler_class=SimpleHTTPRequestHandler):
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

from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl

httpd = HTTPServer(('', 4443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)

try:
    print('starting')
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print('Stoping https server..\n')
import multiprocessing
from multiprocessing import reduction
import socket
import ssl
import signal
import os
import time
import sys

content_dir = '.'
def generate_headers(response_code):
    header = ''
    if response_code == 200:
        header += 'HTTP/1.1 200 OK\r\n'
    elif response_code == 404:
        header += 'HTTP/1.1 404 Not Found\r\n'
        
    time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header += 'Date: {now}\r\n'.format(now=time_now)
    header += 'Server: Simple-Python-Server\r\n'
    header += 'Connection: close\r\n\r\n' # Signal that connection will be closed after completing the request
    return header

def workerFunc(client, address):
    PACKET_SIZE = 1024
    while True:
        print("CLIENT",client)
        data = client.recv(PACKET_SIZE).decode() # Recieve data packet from client and decode
        if not data: break
        request_method = data.split(' ')[0]
        print("Method: {m}".format(m=request_method))
        print("Request Body: {b}".format(b=data))

        if request_method == "GET" or request_method == "HEAD":
            # Ex) "GET /index.html" split on space
            file_requested = data.split(' ')[1]
            # If get has parameters ('?'), ignore them
            file_requested =  file_requested.split('?')[0]
            if file_requested == "/":
                file_requested = '/index.html'

            filepath_to_serve = content_dir + file_requested
            print("Serving web page [{fp}]".format(fp=filepath_to_serve))

            # Load and Serve files content
            try:
                f = open(filepath_to_serve, 'rb')
                if request_method == "GET": # Read only for GET
                    response_data = f.read()
                f.close()
                response_header = generate_headers(200)

            except Exception as e:
                print("File not found. Serving 404 page.")
                response_header = generate_headers(404)

                if request_method == "GET": # Temporary 404 Response Page
                    #response_data = b"<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href="/">dry land</a>.</p></body></html>"
                    response_data = bytes('<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href="/">dry land</a>.</p></body></html>', 'utf-8')
            response = response_header.encode()
            if request_method == "GET":
                response += response_data

            client.send(response)
            client.close()
            break
        else:
            print("Unknown HTTP request method: {method}".format(method=request_method))

class WebServer(object):
    def __init__(self, port=4343):
        self.host = 'localhost'#socket.gethostname().split('.')[0] # Default to any avialable network interface
        self.port = port
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Starting server on {host}:{port}".format(host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
            print("Server started on port {port}.".format(port=self.port))

        except Exception as e:
            print("Error: Could not bind to port {port}".format(port=self.port))
            self.shutdown()
            sys.exit(1)

        self._listen() # Start listening for connections

    def shutdown(self):
        try:
            print("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass # Pass if socket is already closed

    def _listen(self):
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            wkr_pss = multiprocessing.Process(target=workerFunc, args=(client, address,))
            wkr_pss.start()
            wkr_pss.join()

def shutdownServer(sig, unused):
    server.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, shutdownServer)
server = WebServer(4343)
server.start()
print("Press Ctrl+C to shut down server.")

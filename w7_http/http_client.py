import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nAccept: text/html\r\n\r\nConnection: close\r\n\r\n')
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode())
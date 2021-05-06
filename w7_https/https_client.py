import socket
import ssl

host_addr = 'www.tku.edu.tw'
host_port = 443
server_sni_hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established. Peer: {}".format(conn.getpeercert()))
conn.sendall(b"GET / HTTP/1.1\r\nHost: www.tku.edu.tw\r\nConnection: close\r\n\r\n")
new = conn.recv(4096)
print(new)
conn.close()
'''
import socket
import ssl

hostname = 'www.tku.edu.tw'
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        ssock.sendall(b"GET / HTTP/1.1\r\nHost: www.tku.edu.tw\r\nConnection: close\r\n\r\n")
        new = ssock.recv(4096)
        print(new)
'''
'''
import socket
import ssl

hostname = 'www.tku.edu.tw'

with socket.create_connection((hostname, 443)) as sock:
    with ssl.wrap_socket(sock, ca_certs="./server.crt", cert_reqs=ssl.CERT_REQUIRED, certfile="./client.crt", keyfile="./client.key") as ssock:
        ssock.sendall(b"GET / HTTP/1.1\r\nHost: www.tku.edu.tw\r\nConnection: close\r\n\r\n")
        new = ssock.recv(4096)
        print(new)  
'''
'''
import ssl
import socket

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#context.verify_mode = ssl.CERT_REQUIRED
context.load_default_certs()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = context.wrap_socket(s, server_hostname='www.tku.edu.tw')
s.connect(('www.tku.edu.tw', 443))
s.sendall(b"GET / HTTP/1.1\r\nHost: www.tku.edu.tw\r\nConnection: close\r\n\r\n")
while True:
    new = s.recv(4096)
    if not new:
      s.close()
      break
print(new)
'''

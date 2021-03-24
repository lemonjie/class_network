import socket
import time
import hashlib

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#soc.connect(('127.0.0.1', 12345))
soc.connect(('192.168.0.12', 12345))
MAX_BUFFER_SIZE = 4096
MD5_SIZE = 32
ACK = 'ACK'

msg_file = open('test_50MB.txt', 'r')
msg_string = msg_file.read()
msg_bytes = msg_string.encode('utf-8')
msg_file.close()

m = hashlib.md5()
m.update(msg_bytes)
msg_md5 = m.hexdigest()

send_size = 4000
num_send = int(len(msg_bytes) / send_size) + (len(msg_bytes) % send_size > 0)

soc.send(str(len(msg_bytes) + MD5_SIZE).encode('utf-8'))
recv_bytes = soc.recv(MAX_BUFFER_SIZE)
if recv_bytes.decode('utf-8') != ACK:
    print('ACK wrong. ', recv_bytes.decode('utf-8'))

for i in range(0, num_send):
    print('sending ', i)
    if ((i+1)*send_size) >= len(msg_bytes):
        soc.send(msg_bytes[i*send_size:])
    else:
        try:
            soc.send(msg_bytes[i*send_size : (i+1)*send_size])
        except socket.error as msg:
            print('Error : ')

    recv_bytes = soc.recv(MAX_BUFFER_SIZE)
    if recv_bytes.decode('utf-8') != ACK:
        print('ACK wrong. ', recv_bytes.decode('utf-8'))

soc.send(msg_md5.encode('utf-8'))
result_bytes = b''
while len(result_bytes) < 17:
    result_bytes += soc.recv(MAX_BUFFER_SIZE)
result_string = result_bytes.decode("utf8")
soc.close()

print('Result from server :\n', result_string[-17:])
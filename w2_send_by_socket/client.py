import socket
import time
import hashlib

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#soc.connect(('127.0.0.1', 12345))
soc.connect(('192.168.0.12', 12345))

MAX_BUFFER_SIZE = 4096
MD5_SIZE = 32
ACK = 'ACK'
send_size = 4000

#read message which we want to send
msg_file = open('test_50MB.txt', 'r')
msg_string = msg_file.read()
msg_file.close()

#calculate md5 od message
m = hashlib.md5()
msg_bytes = msg_string.encode('utf-8') #calculate md5 should use bytes in python3
m.update(msg_bytes)
msg_md5 = m.hexdigest()


#test how many time does ACK cost
time_start = time.time()
soc.send('ACK'.encode('utf-8'))
soc.recv(MAX_BUFFER_SIZE)
time_end = time.time()
ack_time = (time_end - time_start)/2
print('an ACK cost ', ack_time, 'sec')

#start calculate time
time_start = time.time()
#send length of the whole message in th begining
soc.send(str(len(msg_bytes) + MD5_SIZE).encode('utf-8'))
recv_bytes = soc.recv(MAX_BUFFER_SIZE)

#calculate how many times should client send
num_send = int(len(msg_bytes) / send_size) + (len(msg_bytes) % send_size > 0)
for i in range(0, num_send):
    #keep send message and receive ACK
    if ((i+1)*send_size) >= len(msg_bytes): #send the end of the whole message
        soc.send(msg_bytes[i*send_size:])
    else:
        soc.send(msg_bytes[i*send_size : (i+1)*send_size])
    #print('sending ', i) #just want to see it run
    recv_bytes = soc.recv(MAX_BUFFER_SIZE)
    #if recv_bytes.decode('utf-8') != ACK:
    #    print('ACK wrong. ', recv_bytes.decode('utf-8'))

#send md5
soc.send(msg_md5.encode('utf-8'))
soc.recv(MAX_BUFFER_SIZE)
time_end = time.time()

#receive result and close the connection
result_bytes = b''
while len(result_bytes) < 17:
    result_bytes += soc.recv(MAX_BUFFER_SIZE)
result_string = result_bytes.decode("utf8")
soc.close()
print('Result from server :\n', result_string[-17:])

#calculate time
send_time = time_end - time_start - ack_time
print('send time: ', send_time, ' sec')
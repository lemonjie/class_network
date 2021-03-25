def do_some_stuffs_with_input(input_string):

    #write message(client send) to .txt
    file_write = open('recv_from_client.txt', 'w')
    file_write.write(input_string[:-32]) #final 32 bytes are md5 of the whole message, calculate by client
    file_write.close()

    #calculate md5 of message which receive from client
    import hashlib
    m = hashlib.md5()
    m.update(input_string[:-32].encode('utf-8'))
    md5 = m.hexdigest()

    #check if the two md5 are the same
    if md5 == input_string[-32:]:
        ifsuccess = 'send successfully'
    else:
        ifsuccess = 'something failed.'

    return ifsuccess, md5

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    import sys
    import time

    ACK = 'ACK'
    input_from_client_bytes = b''
    input_from_client_bytes_num = b''
    recv_num = 0
    
    #for test how many time ACK cost
    conn.recv(MAX_BUFFER_SIZE)
    conn.send('ACK'.encode('utf-8'))

    #receive the size of the whole message(bytes) in the begining
    input_from_client_bytes_num = conn.recv(MAX_BUFFER_SIZE)
    conn.send(ACK.encode('utf-8'))
    send_num = int(input_from_client_bytes_num.decode('utf-8'))
    
    while True:

        #keep receive message and send ACK
        input_from_client_bytes_part = conn.recv(MAX_BUFFER_SIZE)
        conn.send(ACK.encode('utf-8'))

        #print(input_from_client_bytes_part.decode('utf-8', 'ignore')[:100]) # just want to see it run
        
        siz = sys.getsizeof(input_from_client_bytes_part)
        if  siz > MAX_BUFFER_SIZE:
            print('The length of input is probably too long: ', siz)
        
        #sum each part of the whole message
        input_from_client_bytes += input_from_client_bytes_part
        #check if length of receive is the same as length of send from client
        recv_num += len(input_from_client_bytes_part)
        if recv_num >= send_num:
            break
    
    #decode message from byte to string
    input_from_client = input_from_client_bytes.decode("utf8")
    #write .txt and check md5
    res, md5 = do_some_stuffs_with_input(input_from_client)
    print(res)

    #send resule to client
    conn.send(res.encode('utf-8'))

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.settimeout(None)
    print('Socket created')

    try:
        soc.bind(("192.168.0.12", 12345))
        #soc.bind(("127.0.0.1", 12345))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    soc.listen(10)
    print('Socket now listening')

    from threading import Thread

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

start_server()

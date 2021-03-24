def do_some_stuffs_with_input(input_string):
    import hashlib
    print('now write txt')
    file_write = open('recv_from_client.txt', 'w')
    file_write.write(input_string[:-32])
    file_write.close()
    print('now calculat md5')
    m = hashlib.md5()
    m.update(input_string[:-32].encode('utf-8'))
    md5 = m.hexdigest()
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

    input_from_client_bytes_num = conn.recv(MAX_BUFFER_SIZE)
    send_num = int(input_from_client_bytes_num.decode('utf-8'))
    conn.send(ACK.encode('utf-8'))
    print(send_num)
    while True:
        input_from_client_bytes_part = conn.recv(MAX_BUFFER_SIZE)
        print('recv ')
        conn.send(ACK.encode('utf-8'))
        print('send ACK')
        siz = sys.getsizeof(input_from_client_bytes_part)
        print(input_from_client_bytes_part.decode('utf-8', 'ignore')[:100])#
        if  siz > MAX_BUFFER_SIZE:
            print('The length of input is probably too long: ', siz)
        input_from_client_bytes += input_from_client_bytes_part
        recv_num += len(input_from_client_bytes_part)
        if recv_num >= send_num:
            break
    print('get all msg.')
    input_from_client = input_from_client_bytes.decode("utf8")

    res, md5 = do_some_stuffs_with_input(input_from_client)
    print('string md5: ', md5)

    conn.send(res.encode('utf-8'))
    #conn.close()
    #print('Connection ' + ip + ':' + port + " ended")

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.settimeout(None)
    print('Socket created')

    try:
        soc.bind(("192.168.0.12", 12345))
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

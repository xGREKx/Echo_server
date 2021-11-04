import socket,getpass,re

def s_send(sock, data, token = ''):
    data = bytearray(f'{len(data)}$@$~{data}$token={token}$'.encode())
    sock.send(data)

def s_recv(sock):
    data = sock.recv(1024).decode()
    indx = data.find('$@$~')
    pswd = data.rfind('$$$~')
    answ = data.rfind('@$$~')
    atkn = re.search('\$token=(.{32,32})\$', data)

    print('Recieved message length - {}'.format(data[:indx]))

    if pswd>-1:
        return data[indx+4:pswd], 1

    elif answ>-1:
        return data[indx+4:answ], 2

    elif atkn:
        indx2 = atkn.start()

        return (data[indx+4:indx2], atkn[1]), 3
    else:
        return data[indx+4:], 0
    

socket.socket.s_send = s_send
socket.socket.s_recv = s_recv





sock = socket.socket()
sock.setblocking(True)
ip_addr,con_port='192.168.1.39',13131
sock.connect((ip_addr, con_port))

while True:
    try:
        data = sock.s_recv()
        if data[1] == 2:
            print(data[0])
            sock.s_send(input('Enter message for server: '), access_token)
        elif data[1] == 1:
            print(data[0])
            sock.s_send(getpass.getpass())
        elif data[1] == 3:
            print(data[0][0])
            print('Token has recieved')
            access_token = data[0][1]
        elif not data[0]:
            print(data[0])
            print('Connection closed...')
            break
        else:
            print(data[0])
    except BlockingIOError:
        pass
        

sock.close()
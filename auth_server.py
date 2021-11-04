import socket,random,csv,hashlib, secrets,re

def s_send(sock, data, service_data=''):
    data = bytearray(f'{len(data)}$@$~{data}{service_data}'.encode())
    sock.send(data)

def s_recv(sock):
    data = sock.recv(1024).decode()
    indx = data.find('$@$~')
    atkn = re.search('\$token=(.{32,32})\$', data)
    if atkn:
        data = data[:atkn.start()]
        atkn = atkn[1]
    else:
        atkn = ''
    print('Recieved message length - {}'.format(data[:indx]))
    return data[indx+4:], atkn

socket.socket.s_send = s_send
socket.socket.s_recv = s_recv

def register(conn, addr, filename):
    conn.s_send('Create password!', '$$$~')
    print('Waiting for new password...')
    password = conn.s_recv()[0]
    with open(filename, 'a', newline = '') as opened_f:
        writer = csv.writer(opened_f, delimiter = ';')
        row=(hashlib.md5(addr[0].encode()).hexdigest(), hashlib.md5(password.encode()).hexdigest())
        writer.writerow(row)
    conn.s_send('You have registered')
    print(f'{addr[0]} have registered')
    return row[1]

def authentification(conn, addr, password, attempts = 3):
    if attempts == 0:
        conn.s_send('You entered invalid password for 3 times')
        return False
    conn.s_send('Enter your password', '$$$~')
    print('Waiting for password...')
    recv_pswd = conn.s_recv()[0]
    if password == hashlib.md5(recv_pswd.encode()).hexdigest():
        access_token = secrets.token_hex(16)

        conn.s_send('You are logged on!','$token='+access_token+"$")
        print(f'{addr[0]} logged on')

        return access_token
    else:
        conn.s_send('invalid password')
        print(f'{addr[0]} entered invalid password')
        authentification(conn, addr, password, attempts-1)
    

def listening(sock):
    print("waiting for the client...")
    while True:
        try:
            conn, addr = sock.accept()
            print(f"connected {addr}")
            break
        except BlockingIOError:
            pass
    pass_file="clients.csv"
    try:
        with open(pass_file, 'r', newline = '') as clients2:
            reader = csv.reader(clients2, delimiter = ';')
            for row in reader:
                if row[0] == hashlib.md5(addr[0].encode()).hexdigest():
                    password = row[1]
                    break
            else:
                password = register(conn, addr, pass_file)

    except FileNotFoundError:
        password = register(conn, addr, pass_file)
    access_token = authentification(conn, addr, password)
    if access_token:
        conn.s_send('Let\'s talk!', '@$$~')
        while True:
            msg = s_recv(conn)
            print(msg[0])
            if msg[1] != access_token:
                print('Warning! Wrong token!')
                break
            if msg[0] == "stop":
                break
            conn.s_send(input("Enter message for client: "), '@$$~')
    else:
        print('Authentification failed!')
        conn.close()
    print(f'Connection with {addr[0]} closed!')

sock = socket.socket()
sock.setblocking(True)
con_port=13131
while True:
    try:
        sock.bind(('', con_port))
        break
    except OSError as oserr:
        print("{} (порт {} занят)".format(oserr,con_port))
        con_port = random.randint(1024,65535)
sock.listen(0)
print('Server is running at port {}'.format(con_port))

for _ in range(5):
    try:
        listening(sock)
    except (ConnectionAbortedError, ConnectionResetError) as err:
        print(err)

sock.close()
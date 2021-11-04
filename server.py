import socket,sys,getpass,random

orig_stdout = sys.stdout
f = open('server_log.txt', 'w')
sys.stdout = f


def listening(sock):
    conn, addr = sock.accept()
    print('Подключен клиент: ', addr)

    with open("clients.txt", 'a+') as clients:
        clients.seek(0,0)
        for line in clients:
            if addr[0] in line:
                conn.send(('Hello '+line.replace(addr[0], '')).encode())
                break
        else:
            conn.send('Enter your name!'.encode())
            username = conn.recv(1024).decode()
            clients.write('\n'+username+addr[0])

    ret=False
    msg = ''

    while True:
        print('Прием данных от клиента')
        try:
            data = conn.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError) as err:
            print(err, addr)
            return
        msg = data.decode()
        print(msg)
        if msg == 'shutdown':
            ret=True
            break
        if not data:
            break
        conn.send(data)
        print('Отправка данных клиенту')
    conn.close()
    print('Отключение клиента:', addr)
    return ret


print('Запуск сервера')
print('''При разрыве соединения сервер продолжает работать
При получении команды shutdown - завершает работу''')
sock = socket.socket()

c_port = 13131
while True:
    try:
        sock.bind(('', c_port))
        print("Подключен к порту {}".format(c_port))
        break
    except OSError as oserr:
        print("{} (порт {} занят)".format(oserr,c_port))
        c_port = random.randint(1024,65535)

sock.listen(0)
print('Начало прослушивания порта')


ret=False
while not ret:
    ret=listening(sock)
print('Остановка сервера')


sys.stdout = orig_stdout
f.close()
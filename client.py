import socket
import getpass

from time import sleep
def try_to_connect(ip_addr, con_port):
    sock = socket.socket()
    sock.settimeout(1)

    print('Попытка соединения с сервером')
    try:
        sock.connect((ip_addr, con_port))
    except ConnectionRefusedError as err:
        print(err)
        return False
    except TypeError:
        return False
    print('Соединение установлено')

    while True:
            try:
                data = sock.recv(1024)
            except socket.timeout:
                break
            print('Успешно принято')
            print(data.decode())


    while True:
        msg = input('Ожидаю ввод сообщения для сервера: ')
        print('Попытка отправить данные серверу:')
        sock.send(msg.encode())
        print('Успешно отправлено')
        if msg == 'exit':
            break
        print('Попытка приема данных от сервера:')
        try:
            data = sock.recv(1024)
        except socket.timeout:
            continue
        print('Успешно принято')
        print(data.decode())   

    sock.close()
    return True

ip_addr= getpass.getpass(prompt = 'Введите IP address: ')
if ip_addr == '':
    ip_addr = '192.168.1.39'
con_port=getpass.getpass(prompt = 'Введите порт: ')
if con_port == '':
    con_port=51815
else:
    try:
        con_port=int(con_port)
    except:
        print('Некорректный порт')

logical=False
count_conn_try=0
while not logical and count_conn_try<5:
    logical=try_to_connect(ip_addr,con_port)
    if not logical:
        count_conn_try+=1
    else:
        count_conn_try=0
if count_conn_try==5:
    print('Сервер недоступен было сделано 5 попыток подключения')
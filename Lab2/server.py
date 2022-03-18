from email.policy import default
import socket, threading
import logging

host = '127.0.0.1'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

command_list = [
    '/disconnect - Отключиться от сервера', 
    '/send <message> - Отправить сообщение', 
    '/logLevel <level> - Устанить уровень логирования', 
    '/help - Список всех команд', 
    '/quit - Разорвать активное подключение'
]

logLevel = {
    "0": "DEBUG",
    "1": "INFO",
    "2": "WARNING",
    "3": "ERROR",
    "4": "CRITICAL"
}

def broadcast(message, client):
    mess = bytes.decode(message, encoding='utf-8')
    command = mess.split(" ")
    if command[0] == '/help':
        for comm in command_list:
            i = str.encode(comm, encoding='utf-8')
            client.send(i)
    if command[0] == '/send':
        message = str.encode(command[1], encoding='utf-8')
        client.send(message)
    if command[0] == '/disconnect':
        message = str.encode("disconnect", encoding='utf-8')
        client.send(message)
    if command[0] == '/logLevel':
        if command[1] == "0":
            logging.basicConfig(level=logging.DEBUG)
            mess = "Текущий уровень логирования: " + logLevel.get(command[1])
            i = str.encode(mess, encoding='utf-8')
            client.send(i)
        if command[1] == "1":
            logging.basicConfig(level=logging.INFO)
            mess = "Текущий уровень логирования: " + logLevel.get(command[1])
            i = str.encode(mess, encoding='utf-8')
            client.send(i)
        if command[1] == "2":
            logging.basicConfig(level=logging.WARNING)
            mess = "Текущий уровень логирования: " + logLevel.get(command[1])
            i = str.encode(mess, encoding='utf-8')
            client.send(i)
        if command[1] == "3":
            logging.basicConfig(level=logging.ERROR)
            mess = "Текущий уровень логирования: " + logLevel.get(command[1])
            i = str.encode(mess, encoding='utf-8')
            client.send(i)
        if command[1] == "4":
            logging.basicConfig(level=logging.ERROR)
            mess = "Текущий уровень логирования: " + logLevel.get(command[1])
            i = str.encode(mess, encoding='utf-8')
            client.send(i)
        else:
            i = str.encode("Такого уровня логированяи не существует", encoding='utf-8')
            client.send(i)
    


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Соединён с {}".format(str(address)))
        clients.append(client)
        client.send('Подключён к серверу!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
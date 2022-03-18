import socket, threading


connect = input("Подключитесь к серверу: ")

command = connect.split(" ")

if command[0] == '/connect':
    ip, port = command[1].split(":")[0], command[1].split(":")[1]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, int(port)))

    def receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "disconnect":
                    print("Вы отключились от сервера для продолжния нажмите любую клавишу...")
                    client.close()
                    break
                else:
                    print("Эхо: " + message)
            except:
                client.close()
                break
        
    def write():
        while True:
            try:
                message = input('')
                client.send(message.encode('utf-8'))
            except:
                break
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()

else:
    print("Вы не подлючилсь к серверу или неправильно указали данные для подключения")

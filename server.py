
import socket  # Импортируем модуль socket для работы с сетевыми соединениями
import logging  # Импортируем модуль logging для ведения лог-файла
 

import sys
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(0)
# Запрашиваем у пользователя номер порта, на котором будет работать сервер
 

port = int(input("port:"))
 

# Настраиваем логирование в файл server.log
 

logging.basicConfig(filename='server.log', level=logging.INFO,
 

                    format='%(asctime)s - %(levelname)s - %(message)s')
 


 

# Функция для безопасного ввода номера порта
 

def get_port():
 

    while True:
 

        try:
 

            # Запрашиваем у пользователя номер порта с возможностью использовать значение по умолчанию
 

            port_input = input("Введите номер порта [по умолчанию 12345]: ")
 

            if not port_input.strip():
 

                # Если пользователь ничего не ввёл, используем порт по умолчанию
 

                port = 12345
 

            else:
 

                port = int(port_input)
 

            if 1 <= port <= 65535:
 

                return port
 

            else:
 

                print("Пожалуйста, введите номер порта от 1 до 65535.")
 

        except ValueError:
 

            print("Некорректный ввод. Пожалуйста, введите числовое значение номера порта.")
 


 

# Получаем номер порта от пользователя
 

port = get_port()
 

# Создаем TCP/IP сокет
 

# socket.AF_INET означает, что будем использовать сетевой протокол IPv4
 

# socket.SOCK_STREAM означает, что будем использовать протокол TCP (потоковый)
 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 


 

# Устанавливаем опцию сокета SO_REUSEADDR
 

# Это позволяет повторно использовать локальный адрес при повторном запуске сервера
 

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 


 

# Привязываем сокет к указанному адресу и порту
 

# Пустая строка '' или '0.0.0.0' как адрес означает, что сервер будет принимать соединения на всех сетевых интерфейсах
 

sock.bind(('', port))
 

# Пытаемся привязать сокет к указанному адресу и порту
 

# Если порт занят, автоматически выбираем новый порт
 

while True:
 

    try:
 

        # Привязываем сокет к указанному адресу и порту
 

        # Пустая строка '' означает, что сервер будет принимать соединения на всех сетевых интерфейсах
 

        sock.bind(('', port))
 

        break  # Если привязка успешна, выходим из цикла
 

    except OSError as e:
 

        if e.errno == 98:  # Код ошибки "адрес уже используется"
 

            logging.warning(f"Порт {port} уже занят, пробуем следующий порт.")
 

            port += 1  # Увеличиваем номер порта и пробуем снова
 

        else:
 

            logging.error(f"Ошибка при попытке привязать сокет к порту {port}: {e}")
 

            sys.exit(1)  # Завершаем программу при других ошибках
 


 

# Выводим в консоль номер порта, который сервер слушает
 

print(f"Сервер слушает порт {port}")
 

print("Server is starting")  # пункт 2.i выполнен
 
logging.info("Server is starting")  # Записываем в лог вместо вывода в консоль

 

# Начинаем прослушивание входящих соединений
 

# Параметр 1 определяет максимальное число подключений в очереди (backlog)
 
# Параметр 1 определяет максимальное число подключений в очереди
sock.listen(1)
 

print("Port", port, "is listening")  # пункт 2.ii выполнен
 
logging.info(f"Port {port} is listening")  # Записываем в лог

 



# Основной цикл сервера для принятия и обработки клиентов
 

while True:
 

    try:
 

        # Метод accept() блокирует выполнение программы до установления входящего соединения
 

        # После установления соединения возвращает новый сокет conn для общения с клиентом и адрес клиента addr
 

        conn, addr = sock.accept()
 

        print("Client is accepted")  # пункт 2.iii выполнен
 

        print("Client address:", addr[0])  # Выводим IP-адрес клиента
 

        print("Client port:", addr[1])     # Выводим порт клиента 

        logging.info("Client is accepted")  # Записываем в лог
 

        logging.info(f"Client address: {addr[0]}")  # Записываем IP-адрес клиента в лог
 

        logging.info(f"Client port: {addr[1]}")     # Записываем порт клиента в лог

       # Инициализируем переменную msg для накопления полученных данных от клиента
 

        msg = ''

# Основной цикл работы с клиентом
while True:
	data = conn.recv(1024)
	if not data:
		break
	msg += data.decode()
	conn.send(data)

print(msg)
# Получаем данные от клиента
 

    data = conn.recv(1024)
 

    if not data:
 

        # Если метод recv() вернул пустые данные, это означает, что клиент закрыл соединение
 

        print("All data is accepted")  # пункт 2.iv выполнен
 
                logging.info("All data is accepted")  # Записываем в лог
        break
 

    # Декодируем полученные байты в строку
 

    msg += data.decode('utf-8')
 

    # Проверяем, есть ли в накопленных данных полное сообщение
 

    while '\n' in msg:
 

        # Разделяем данные по символу новой строки '\n'
 

        line, msg = msg.split('\n', 1)
 

        print(f"Received from client: {line}")  # Выводим полное сообщение от клиента
 
                logging.info(f"Received from client: {line}")  # Записываем полученное сообщение в лог
        if line.lower() == 'exit':
 

            # Если клиент отправил команду 'exit', завершаем работу с клиентом
 

            print("Exit command received. Closing connection.")
 
                    logging.info("Exit command received. Closing connection.")
            # Отправляем подтверждение клиенту перед закрытием соединения
 

            conn.send("Server closing connection.\n".encode('utf-8'))
 

            break
 

        else:
 

            # Обрабатываем полученное сообщение
 

            # Для примера переведем строку в верхний регистр
 

            response = line.upper()
 

            # Отправляем ответ клиенту, добавляя символ '\n' в конце
 

            conn.send((response + '\n').encode('utf-8'))
 

            print("Response sent to client")  # Подтверждаем отправку ответа
 
                    logging.info("Response sent to client")  # Записываем в лог
    if line.lower() == 'exit':
 

        # Если была получена команда 'exit', выходим из внешнего цикла
 

        break
        # Цикл для общения с подключенным клиентом
 

        while True:
 

            # Получаем данные от клиента
 

            data = conn.recv(1024)
 

            if not data:
 

                # Если метод recv() вернул пустые данные, это означает, что клиент закрыл соединение
 

                print("All data is accepted")  # пункт 2.iv выполнен
 

                break  # Выходим из внутреннего цикла для ожидания нового клиента
 

            # Декодируем полученные байты в строку
 

            msg += data.decode('utf-8')
 

            # Проверяем, есть ли в накопленных данных полное сообщение
 

            while '\n' in msg:
 

                # Разделяем данные по символу новой строки '\n'
 

                line, msg = msg.split('\n', 1)
 

                print(f"Received from client: {line}")  # Выводим полное сообщение от клиента
 

                if line.lower() == 'exit':
 

                    # Если клиент отправил команду 'exit', завершаем работу с этим клиентом
 

                    print("Exit command received. Closing connection.")
 

                    # Отправляем подтверждение клиенту перед закрытием соединения
 

                    conn.send("Server closing connection.\n".encode('utf-8'))
 

                    break  # Выходим из внутреннего цикла общения с клиентом
 

                else:
 

                    # Обрабатываем полученное сообщение
 

                    # Для примера переведем строку в верхний регистр
 

                    response = line.upper()
 

                    # Отправляем ответ клиенту, добавляя символ '\n' в конце
 

                    conn.send((response + '\n').encode('utf-8'))
 

                    print("Response sent to client")  # Подтверждаем отправку ответа
 

            if line.lower() == 'exit':
 

                break  # Выходим из внутреннего цикла общения с клиентом

# После выхода из цикла закрываем соединение с клиентом
conn.close()
print("Connection is closed. Client is off")  # пункт 2.vi выполнен
 

        logging.info("Connection is closed. Client is off")  # Записываем в лог
        # После выхода из цикла общения с клиентом закрываем соединение
 

        conn.close()
 

        print("Connection is closed. Client is off")  # пункт 2.vi выполнен
 

        # Возвращаемся к началу внешнего цикла для принятия нового клиента
 

        print("Waiting for new client...")
 
        logging.info("Waiting for new client...")

    except KeyboardInterrupt:
 

        # Позволяет остановить сервер с клавиатуры (например, нажатием Ctrl+C)
 

        print("\nServer is shutting down.")
 
        logging.info("Server is shutting down.")
 

        print("\nСервер завершает работу.")
        break  # Выходим из основного цикла сервера 
    except Exception as e:
 

        logging.error(f"An error occurred: {e}")
# Закрываем главный серверный сокет
# После выхода из основного цикла закрываем главный серверный сокет

sock.close()
 

print("Server is off")  # пункт 2.vii выполнен
logging.info("Server is off")  # Записываем в лог

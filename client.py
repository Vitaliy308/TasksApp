import socket
import json


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 3008))

    print("[INFO] Подключен к серверу.")

    user = input("Введите свой никнейм: ")
    client_socket.send(json.dumps({'action': 'login', 'user': user}).encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Ответ: {response}")

    while True:
        print("1. Добавить задачу")
        print("2. Список задач")
        print("3. Завершить задачу")
        choice = input("Выберите действие: ")

        if choice == '1':
            task = input("Введите название задачи: ")
            priority = input("Ввведите приоритет (low/medium/high): ")
            deadline = input("Укажите дедлайн (необязательно): ")
            description = input("Ввведите описание задачи (необязательно): ")

            request = json.dumps({
                'action': 'add',
                'task': task,
                'priority': priority,
                'deadline': deadline,
                'description': description
            })
        elif choice == '2':
            request = json.dumps({'action': 'list'})
        elif choice == '3':
            task = input("Введите название задачи для завершения: ")
            request = json.dumps({'action': 'complete', 'task': task})
        else:
            print("Неверный выбор.")
            continue

        client_socket.send(request.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ: {response}")


if __name__ == "__main__":
    client()

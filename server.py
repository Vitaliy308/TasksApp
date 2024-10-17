import socket
import threading
import json

users_tasks = {}


def handle_client(client_socket):
    user = None

    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            print(f"[INFO] Полученный запрос: {json.dumps(json.loads(request), ensure_ascii=False)}")

            data = json.loads(request)
            action = data.get('action')

            if action == 'login':
                user = data.get('user')
                if user not in users_tasks:
                    users_tasks[user] = []
                client_socket.send(f"Пользователь '{user}' вошел в систему.".encode('utf-8'))

            elif user:
                if action == 'add':
                    task = {
                        'task': data.get('task'),
                        'priority': data.get('priority', 'low'),
                        'deadline': data.get('deadline', 'none'),
                        'description': data.get('description', ''),
                        'completed': False
                    }
                    users_tasks[user].append(task)
                    response = f"Задача '{task['task']}' добавлена!"
                elif action == 'list':
                    response = json.dumps(users_tasks[user], indent=4, ensure_ascii=False)
                elif action == 'complete':
                    task_name = data.get('task')
                    for t in users_tasks[user]:
                        if t['task'] == task_name:
                            t['completed'] = True
                            response = f"Задача '{task_name}' помеча выполненной!"
                            break
                    else:
                        response = f"Задача '{task_name}' не найдена."
                else:
                    response = "Неизвестное действие."
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("Пожалуйста, сначала войдите в систему.".encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] {e}")
            break


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 3008))
    server_socket.listen(5)
    print("[INFO] Сервер запущен и слушает...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[INFO] Соединение установлено с {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    server()

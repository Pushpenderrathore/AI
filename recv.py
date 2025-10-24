import socket

HOST = "127.0.0.1"  # change to your server IP
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(s.recv(1024).decode('utf-8'), end='')
    while True:
        msg = input(">>> ")
        if msg.lower() in {"exit", "quit"}:
            break
        s.send((msg + "\n").encode('utf-8'))
        data = s.recv(4096).decode('utf-8', errors='ignore')
        print(data)

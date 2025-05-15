import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

while True:
    message = input("Send to server: ")
    client.send(message.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    print(f"Server replied: {data}")

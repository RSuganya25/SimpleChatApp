import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(1)

print("Server is listening on port 5555...")

conn, addr = server.accept()
print(f"Connection established with {addr}")

while True:
    data = conn.recv(1024).decode('utf-8')
    if not data:
        break
    print(f"Client says: {data}")
    message = input("Reply to client: ")
    conn.send(message.encode('utf-8'))

conn.close()

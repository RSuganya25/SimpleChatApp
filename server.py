import socket
from datetime import datetime

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

    # Respond based on client message
    if data.lower() == "greet":
        response = "Hello! The current time is " + datetime.now().strftime("%H:%M:%S")
    elif data.lower() == "exit":
        response = "Goodbye!"
        conn.send(response.encode('utf-8'))
        break
    else:
        response = "I don't understand that command."

    conn.send(response.encode('utf-8'))

conn.close()
print("Connection closed.")

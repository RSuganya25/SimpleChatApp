import socket

HOST = 'localhost'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server. Type messages or 'exit' to quit.")

while True:
    message = input("Send to server: ").strip()
    if not message:
        continue

    client.send(message.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    print(f"Server replied: {data}")

    if message.lower() == "exit":
        break

client.close()
print("Connection closed.")

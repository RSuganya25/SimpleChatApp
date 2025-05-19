import socket
import json

HOST = 'localhost'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connected to server. Send JSON commands. Type 'exit' to quit.")

def send_request(req: dict):
    """Send a JSON request and return a parsed JSON response."""
    client.send(json.dumps(req).encode('utf-8'))
    raw = client.recv(1024).decode('utf-8')
    return json.loads(raw)

while True:
    cmd = input("Enter command (greet, math <expr>, exit): ").strip()
    if not cmd:
        continue

    if cmd.lower() == "exit":
        response = send_request({"type": "exit"})
        print("Server replied:", response)
        break

    parts = cmd.split(maxsplit=1)
    if parts[0].lower() == "greet":
        request = {"type": "greet"}

    elif parts[0].lower() == "math" and len(parts) == 2:
        request = {"type": "math", "expression": parts[1]}

    else:
        print("Invalid command format.")
        continue

    response = send_request(request)
    print("Server replied:", response)

client.close()
print("Connection closed.")

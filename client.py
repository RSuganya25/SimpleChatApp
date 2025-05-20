import socket
import json

HOST = 'localhost'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connected to server. Send JSON commands. Type 'exit' to quit.")

def send_request(req: dict):
    """Send a JSON request and return parsed JSON response."""
    client.send(json.dumps(req).encode('utf-8'))
    raw = client.recv(1024).decode('utf-8')
    return json.loads(raw)

while True:
    cmd = input("Enter command (greet, math <expr>, exit, list, send <target> <msg>): ").strip()
    if not cmd:
        continue

    parts = cmd.split(maxsplit=2)
    cmd_type = parts[0].lower()

    if cmd_type == "exit":
        request = {"type": "exit"}

    elif cmd_type == "greet":
        request = {"type": "greet"}

    elif cmd_type == "math" and len(parts) == 2:
        request = {"type": "math", "expression": parts[1]}

    elif cmd_type == "list":
        request = {"type": "list"}

    elif cmd_type == "send" and len(parts) == 3:
        request = {"type": "send", "target": parts[1], "message": parts[2]}

    else:
        print("Invalid command or format.")
        continue

    response = send_request(request)
    print("Server replied:", response)

    if cmd_type == "exit":
        break

client.close()
print("Connection closed.")

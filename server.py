import socket
import threading
import json
from datetime import datetime

HOST = 'localhost'
PORT = 5555

# Create and configure the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"[LISTENING] Server is listening on {HOST}:{PORT}...")

def handle_client(conn, addr):
    """Handle communication with a single client."""
    print(f"[CONNECTED] {addr}")
    while True:
        try:
            raw = conn.recv(1024).decode('utf-8')
            if not raw:
                break

            # Parse JSON request
            try:
                request = json.loads(raw)
            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON"}
                conn.send(json.dumps(response).encode('utf-8'))
                continue

            msg_type = request.get("type", "").lower()
            print(f"[{addr}] Request: {request}")

            # Handle request types
            if msg_type == "greet":
                reply = {
                    "status": "ok",
                    "message": "Hello!",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

            elif msg_type == "math":
                expr = request.get("expression", "")
                try:
                    # WARNING: eval can be dangerous — placeholder for safe eval
                    result = eval(expr, {"__builtins__": {}})
                    reply = {"status": "ok", "result": result}
                except Exception as e:
                    reply = {"status": "error", "message": str(e)}

            elif msg_type == "exit":
                reply = {"status": "ok", "message": "Goodbye!"}
                conn.send(json.dumps(reply).encode('utf-8'))
                break

            else:
                reply = {"status": "error", "message": "Unknown command"}

            # TODO May 20: if msg_type == "data": load from file or database here

            conn.send(json.dumps(reply).encode('utf-8'))

        except ConnectionResetError:
            # Client disconnected abruptly
            break
        except Exception as e:
            print(f"[ERROR] {addr} - {e}")
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

# Main loop: accept new clients and spawn a thread for each
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

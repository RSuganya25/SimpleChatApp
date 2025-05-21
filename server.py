import socket
import threading
import json
from datetime import datetime

HOST = 'localhost'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"[LISTENING] Server is listening on {HOST}:{PORT}...")

clients = {}  # map: addr_str -> (conn, addr)

lock = threading.Lock()

def broadcast(message, exclude=None):
    """Send a JSON message to all clients except 'exclude'."""
    with lock:
        for addr_str, (conn, _) in clients.items():
            if addr_str != exclude:
                try:
                    conn.send(json.dumps(message).encode('utf-8'))
                except:
                    pass

def handle_client(conn, addr):
    addr_str = f"{addr[0]}:{addr[1]}"
    with lock:
        clients[addr_str] = (conn, addr)
    print(f"[CONNECTED] {addr_str}")

    # Broadcast join message
    broadcast({"type": "info", "message": f"{addr_str} has joined the chat."}, exclude=addr_str)

    try:
        while True:
            raw = conn.recv(1024).decode('utf-8')
            if not raw:
                break

            try:
                request = json.loads(raw)
            except json.JSONDecodeError:
                conn.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode('utf-8'))
                continue

            msg_type = request.get("type", "").lower()
            print(f"[{addr_str}] Request: {request}")

            if msg_type == "greet":
                reply = {
                    "status": "ok",
                    "message": "Hello!",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

            elif msg_type == "math":
                expr = request.get("expression", "")
                try:
                    # Evaluate math expression safely - only basic arithmetic
                    allowed_chars = "0123456789+-*/(). "
                    if any(c not in allowed_chars for c in expr):
                        raise ValueError("Invalid characters in expression")
                    result = eval(expr, {"__builtins__": {}})
                    reply = {"status": "ok", "result": result}
                except Exception as e:
                    reply = {"status": "error", "message": str(e)}

            elif msg_type == "list":
                with lock:
                    count = len(clients)
                reply = {"type": "info", "message": f"Currently {count} client(s) connected."}

            elif msg_type == "send":
                target = request.get("target", "")
                message = request.get("message", "")
                with lock:
                    if target in clients:
                        target_conn, _ = clients[target]
                        try:
                            target_conn.send(json.dumps({
                                "type": "message",
                                "from": addr_str,
                                "message": message
                            }).encode('utf-8'))
                            reply = {"status": "ok", "message": "Message sent."}
                        except Exception as e:
                            reply = {"status": "error", "message": f"Failed to send message: {e}"}
                    else:
                        reply = {"status": "error", "message": "Target client not found."}

            elif msg_type == "exit":
                reply = {"status": "ok", "message": "Goodbye!"}
                conn.send(json.dumps(reply).encode('utf-8'))
                break

            else:
                reply = {"status": "error", "message": "Unknown command"}

            conn.send(json.dumps(reply).encode('utf-8'))

    except ConnectionResetError:
        print(f"[DISCONNECTED ABRUPT] {addr_str}")
    except Exception as e:
        print(f"[ERROR] {addr_str} - {e}")

    # Client disconnect cleanup
    with lock:
        if addr_str in clients:
            del clients[addr_str]
    print(f"[DISCONNECTED] {addr_str}")

    # Broadcast leave message
    broadcast({"type": "info", "message": f"{addr_str} has left the chat."}, exclude=addr_str)

    conn.close()
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()
    with lock:
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")

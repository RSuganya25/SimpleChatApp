import socket
import threading
from datetime import datetime

HOST = 'localhost'
PORT = 5555

# Create and configure the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server is listening on {HOST}:{PORT}...")

def handle_client(conn, addr):
    """Handle communication with a single client."""
    print(f"[CONNECTED] {addr}")
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[{addr}] Client says: {data}")

            # Respond based on client message
            msg = data.lower().strip()
            if msg == "greet":
                response = "Hello! The current time is " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif msg == "exit":
                response = "Goodbye!"
                conn.send(response.encode('utf-8'))
                break
            else:
                response = "I don't understand that command."

            conn.send(response.encode('utf-8'))

        except ConnectionResetError:
            # Client disconnected abruptly
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

# Main loop: accept new clients and spawn a thread for each
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()

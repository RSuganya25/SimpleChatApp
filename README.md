## Overview

**Project Title**:  
Python Socket Client-Server Chat App

**Project Description**:  
A Python socket-based program that demonstrates a simple yet expandable client-server architecture. The client sends structured JSON requests, and the server responds accordingly. This project introduces core networking concepts using TCP sockets while also exploring JSON, threading, and basic request handling.

**Project Goals**:  
•	Understand socket communication in Python
•	Build a TCP-based multi-client chat-style app
•	Use structured JSON messages for clear communication
•	Handle client disconnections gracefully and keep server alive
•	Support multiple types of client requests (greet, math, exit)
•	Manage multiple clients concurrently using threads
•	Enable clients to:
   o	See how many clients are connected (list)
   o	Send messages directly to other clients (send <target> <message>)
   o	Receive broadcast messages when clients join or leave
•	Maintain clean code and track features via GitHub
•	Prepare for future enhancements like file/database interaction

## Instructions for Build and Use

**Steps to build and run the software:**

1. Clone this repository from GitHub  
2. In one terminal, run `server.py` to start the server  
3. In separate terminals, run `client.py` to launch one or more clients  

**Usage Instructions:**

1. After running both scripts, follow prompts in the client terminal  
2. Enter a command from the supported types below:  
   - `greet`  
     - Returns a welcome message with the current server date/time  
   - `math <expression>`  
     - Evaluates the expression (e.g., `math 5 + 2 * 3`)  
   - `list`
     - Shows the number of currently connected clients  
   - `send <target_addr> <message>`
     - Sends a message to the client identified by <target_addr> (format: IP:port)  
   - `exit`  
     - Ends the session with a goodbye message  
3. When a client joins or leaves, all connected clients receive a broadcast notification
3. The server responds with JSON-formatted output for clarity
4. You can close clients and reconnect to test real-time interaction and message delivery  

## Example Commands and Responses
Input from Client: greet

Server Response: {"status": "ok", "message": "Hello!", "time": "2025-05-19 18:40:12"}

Input from Client: math 7 * (2 + 3)

Server Response: {"status": "ok", "result": 35}

Input from Client: list

Server Response: {"type": "info", "message": "Currently 3 client(s) connected."}

Input from Client: send 127.0.0.1:59329 Hello there!

Server Response: {"status": "ok", "message": "Message sent to 127.0.0.1:59329"}

Input from Client: exit

Server Response: {"status": "ok", "message": "Goodbye!"}
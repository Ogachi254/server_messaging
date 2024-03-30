## Messaging Server Simulator

This project implements a simulator of a messaging server using TCP/IP sockets in Python. It allows multiple node objects (clients) to connect to a server object via the local host TCP/IP interface, enabling inter-node communication with all data transmission routed through the server.

## Project Description
# Overview
The project comprises two main components: a server and multiple nodes. The server opens a listening socket to allow nodes to connect to it and spawns worker threads as needed to facilitate inter-node communication. Nodes connect to the server, send data, and receive messages from other nodes via the server.
# Main Class
The main class instantiates a single server and multiple nodes based on command-line arguments. It manages the overall flow of the program, ensuring all nodes finish sending data before shutting down the server and nodes cleanly.

# Server Class
The server class represents the central server entity. It manages client connections, handles inter-node communication, and maintains a table of connected clients. The server is capable of handling multiple nodes sending data simultaneously.

# Node Class (Clients)
The node class represents the individual clients connecting to the server. Each node connects to the server upon startup, sends data to other nodes via the server, and prints received messages.

## How to Run
Clone the Repository: git clone https://github.com/Ogachi254/server_messaging.git 

Navigate to the Project Directory:

cd messaging-server-simulator

# Run the Server:

python3 server.py

# Run the Nodes:

python3 node.py

Repeat the above command for each node you want to simulate.

Follow on-screen Instructions:

Input messages as prompted by the nodes.
View received messages printed by the nodes.

Shut Down the Server and Nodes:

Once all nodes have finished sending data, press Ctrl+C to shut down the server and nodes cleanly.

## Requirements
Python 3.x
Standard Python libraries (socket, threading, queue)

## Note

Ensure that the server and nodes are run on the same machine and network for local communication.
Customize the server and node configurations as needed by modifying the code or command-line arguments.
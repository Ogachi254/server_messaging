import socket
import threading
import queue
import sys

class Server:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}
        self.frame_buffer = queue.Queue()
        self.lock = threading.Lock()

    def start(self):
        self.sock.bind(('localhost', self.port))
        self.sock.listen(5)
        print("Server is listening on port", self.port)
        while True:
            conn, addr = self.sock.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

    def handle_client(self, conn, addr):
        with self.lock:
            self.connections[addr] = conn
        print("Connected to", addr)
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print("Received:", data)
                # Forward data to other nodes
                self.forward_data(data, addr)
            except Exception as e:
                print("Error:", e)
                break
        with self.lock:
            del self.connections[addr]
            conn.close()
        print("Connection closed with", addr)

    def forward_data(self, data, sender_addr):
        with self.lock:
            for addr, conn in self.connections.items():
                if addr != sender_addr:
                    conn.sendall(data.encode())

class Node:
    def __init__(self, node_id, server_port):
        self.node_id = node_id
        self.server_port = server_port

    def start(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('localhost', self.server_port))
        print("Node", self.node_id, "connected to server")
        while True:
            try:
                message = input("Node {}: Enter message: ".format(self.node_id))
                conn.sendall(message.encode())
            except Exception as e:
                print("Error:", e)
                break
        conn.close()

def main():
    if len(sys.argv) < 3:
        print("Usage: python program.py server_port node_count")
        return

    server_port = int(sys.argv[1])
    node_count = int(sys.argv[2])

    server = Server(server_port)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    nodes = []
    for i in range(node_count):
        node = Node(i+1, server_port)
        node_thread = threading.Thread(target=node.start)
        node_thread.start()
        nodes.append(node)

    for node in nodes:
        node_thread.join()

    server_thread.join()

if __name__ == "__main__":
    main()

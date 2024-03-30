import socket
import threading
import logging

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.lock = threading.Lock()
        self.logger = logging.getLogger("server")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def handle_client(self, client_socket, addr):
        self.logger.info(f"New connection from {addr}")
        with self.lock:
            self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    self.logger.info("Connection closed by client")
                    break
                self.logger.info(f"Received message from {addr}: {message}")
                self.broadcast(message, client_socket)
            except ConnectionResetError:
                self.logger.error("Connection closed unexpectedly")
                break
        with self.lock:
            self.clients.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message.encode())
                    except Exception as e:
                        self.logger.error(f"Error broadcasting message: {e}")
                        client_socket.close()
                        self.clients.remove(client_socket)

    def start(self):
        self.logger.info(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
        except KeyboardInterrupt:
            self.logger.info("Server shutting down...")
            for client_socket in self.clients:
                client_socket.close()
            self.server_socket.close()

if __name__ == "__main__":
    server = Server('localhost', 12345) 
    server.start()

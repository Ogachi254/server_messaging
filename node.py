import socket
import logging

class Node:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger("node")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def connect_to_server(self):
        try:
            self.socket.connect((self.server_host, self.server_port))
            self.logger.info(f"Connected to server at {self.server_host}:{self.server_port}")
        except ConnectionRefusedError:
            self.logger.error("Connection refused. Server may be unavailable.")
            raise

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
            self.logger.info("Message sent successfully")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise

    def receive_message(self):
        try:
            received_data = self.socket.recv(1024).decode()
            while received_data.endswith('\n'):
                received_data += self.socket.recv(1024).decode()
            self.logger.info(f"Received message: {received_data}")
            return received_data
        except Exception as e:
            self.logger.error(f"Error receiving message: {e}")
            raise
        
    def close_connection(self):
        self.socket.close()
        self.logger.info("Connection closed")

if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 12345  
    node = Node(server_host, server_port)
    try:
        node.connect_to_server()
        while True:
            message = input("Enter message: ")
            node.send_message(message)
            response = node.receive_message()
            print("Server response:", response)
            send_another = input("Send another message? (y/n): ").lower()
            if send_another != 'y':
                break
    except KeyboardInterrupt:
        node.logger.info("Operation interrupted.")
    finally:
        node.close_connection()


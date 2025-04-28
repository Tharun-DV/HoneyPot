import socket
import threading
import time
import os

class MySQLHoneypot:

    def __init__(self, port=3306, banner_file="mysql_banner.txt", log_dir="logs"):
        self.port = port
        self.banner = self.load_banner(banner_file)
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick restart

    def load_banner(self, banner_file):
        try:
            with open(banner_file, "r") as f:
                banner = f.read().encode() # Encode to bytes
        except FileNotFoundError:
            banner = b"\x56\x00\x00\x00\x0a\x35\x2e\x37\x2e\x33\x36\x2d\x30\x75\x62\x75\x6e\x74\x75\x30\x2e\x32\x30\x2e\x30\x34\x2e\x31\x2d\x6c\x6f\x67\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x72\x34\x4b\x79\x51\x57\x6c\x30\x34\x63\x55\x48\x36\x6d\x70\x71\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00" # Default banner
        return banner



    def run(self):
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        print(f"MySQL Honeypot listening on port {self.port}")
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"[+] Connection from {client_address[0]}:{client_address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()


    def handle_client(self, client_socket, client_address):
        log_filename = os.path.join(self.log_dir, f"mysql_{time.strftime('%Y%m%d_%H%M%S')}_{client_address[0]}.log")
        with open(log_filename, "wb") as log_file:  # Open in binary write mode
            try:
                client_socket.sendall(self.banner)
                log_file.write(self.banner) # Log the banner sent

                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    log_file.write(data)  # Log the raw bytes received
                    # Here, you could add logic to respond to specific commands if you want.
                    # For a simple honeypot, just receiving and logging is often enough.
                
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
            finally:
                client_socket.close()
                print(f"[-] Connection closed from {client_address[0]}:{client_address[1]}")




if __name__ == "__main__":
    honeypot = MySQLHoneypot()
    honeypot.run()

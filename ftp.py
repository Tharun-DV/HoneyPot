import asyncore
import socket
import os
import time
from mail import send_mail

class FTPHoneyPot(asyncore.dispatcher):

    def __init__(self, host, port, banner_file="welcome.txt", log_dir="logs"):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)  # Listen for up to 5 connections
        self.banner = self.load_banner(banner_file)
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def load_banner(self, banner_file):
        try:
            with open(banner_file, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "220 (vsFTPd 3.0.3)"  # Default banner

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print(f"[+] Connection from {addr[0]}:{addr[1]}")
            handler = FTPConnectionHandler(sock, self.log_dir)


class FTPConnectionHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, log_dir):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.log_file = os.path.join(log_dir, f"ftp_{time.strftime('%Y%m%d_%H%M%S')}_{self.addr[0]}.log")  # Unique log file per connection
        self.log(f"Connection from {self.addr[0]}:{self.addr[1]}")
        self.send(b"220 (vsFTPd 3.0.3)\r\n")  # Send initial banner

    def handle_read(self):
        data = self.recv(4096).decode("utf-8", errors="ignore")  # Decode with error handling
        self.log(f"< {data.strip()}")  # Log incoming data
        self.process_command(data)


    def process_command(self, data):
        command = data.split()[0].upper()
        if command == "USER":
            self.send(b"331 Please specify the password.\r\n")
        elif command == "PASS":
            self.send(b"230 Login successful.\r\n")
        # Implement other FTP commands as needed (e.g., PWD, CWD, LIST, RETR)
        #  or simply keep responding with generic success/failure messages
        elif command in ["PWD", "CWD", "LIST", "RETR", "STOR", "DELE"]:  # Example: Respond with dummy data
            self.send(b"250 Okay.\r\n")  # or 550 if you want to simulate failure.
        else:
            self.send(b"500 Unknown command.\r\n")


    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


    def handle_close(self):
        self.log(f"Connection closed from {self.addr[0]}:{self.addr[1]}")
        self.close()



if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all interfaces
    port = 21  # Standard FTP port
    honeypot = FTPHoneyPot(host, port)
    print(f"FTP Honeypot listening on {host}:{port}")
    asyncore.loop()

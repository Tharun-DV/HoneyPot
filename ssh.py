import paramiko
import threading
import socket
import logging

# Configure logging
logging.basicConfig(filename='logs/honeypot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Honeypot configuration
HONEYPOT_PORT = 2222  # Use a non-standard port
HOST_KEY = paramiko.RSAKey.generate(2048) # Generate a host key. Store for future use if desired for consistency.

class SSHHoneyPot(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logging.info(f"Login attempt: username={username}, password={password}") # Log the credentials

        # You might want to save the login attempt details for later analysis
        # E.g., store it in a database or send a notification
        with open('logs/login_attempts.txt', 'a') as f:
            f.write(f'{username}:{password}\n')



        # Always return authentication failed to keep the attacker engaged (optionally)
        # In real use-cases, consider delaying the failure response or adding other interaction.
        return paramiko.AUTH_FAILED


    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                   pixelheight, modes):
        return True


def start_honeypot():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', HONEYPOT_PORT))
        sock.listen(100)
        logging.info(f"Honeypot listening on port {HONEYPOT_PORT}")


        while True:
            client_socket, client_address = sock.accept()
            logging.info(f"Connection from: {client_address}")

            transport = paramiko.Transport(client_socket)
            transport.add_server_key(HOST_KEY)

            server = SSHHoneyPot()
            try:

                transport.start_server(server=server)

                # (optional) interact a bit
                # This allows us to emulate a simple shell, for a more engaging honeypot.
                channel = transport.accept(20)  # Adjust timeout as needed
                if channel is not None:
                    channel.send("\r\nWelcome to the fake server!\r\n")  # Send a greeting or other output

                    # Interact here (e.g., a very basic command processing loop)

                    while True:  # Main shell interaction loop
                         channel.send("$ ")
                         try:
                              command = channel.recv(1024).decode() # Arbitrary receive size; adjust if needed

                              if command.strip() == 'exit': #Example 'exit' command handling. Extend as needed
                                     break

                              channel.send("Command not found: " + command + "\r\n")

                         except Exception as inner_ex:  # Socket closed etc.
                             logging.error(f"Error in shell interaction: {inner_ex}")
                             break
                    channel.close()
                


            except Exception as e:
                logging.error(f"SSH negotiation failed: {e}")

            finally:
                transport.close()

    except Exception as e:
        logging.error(f"Honeypot failed to start: {e}")

if __name__ == "__main__":
    start_honeypot()

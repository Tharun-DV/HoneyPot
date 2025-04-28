import http.server
import socketserver
import os
import time
import threading  # For optional timed log flushing

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override the default logging to write to a file
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "http_honeypot.log")

        # Add timestamp to log message
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {self.client_address[0]} - {format % args}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)



class HTTPServerHoneypot:
    def __init__(self, port=80, handler_class=HTTPRequestHandler, bind_address="0.0.0.0", log_flush_interval=None):
        self.port = port
        self.handler_class = handler_class
        self.bind_address = bind_address
        self.httpd = None  # The actual HTTP server
        self.log_flush_interval = log_flush_interval
        self.log_flush_timer = None


    def start(self):
        with socketserver.TCPServer((self.bind_address, self.port), self.handler_class) as httpd:
            self.httpd = httpd
            print(f"HTTP Honeypot listening on {self.bind_address}:{self.port}")

            if self.log_flush_interval:
                self.start_log_flush_timer()


            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down honeypot...")
            finally:
                if self.log_flush_timer:  # Stop the timer if it was running
                    self.log_flush_timer.cancel()


    def start_log_flush_timer(self):
        self.log_flush_timer = threading.Timer(self.log_flush_interval, self.flush_logs)
        self.log_flush_timer.start()

    def flush_logs(self):
        print("Flushing logs (simulated)") #  Remove in real honeypot
        self.start_log_flush_timer()



if __name__ == "__main__":
    honeypot = HTTPServerHoneypot(port=8080, log_flush_interval=60)  # Log flush every 60 seconds (optional)
    honeypot.start()

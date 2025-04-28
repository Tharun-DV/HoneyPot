import subprocess
import os
import signal
import sys

processes = []

def start_honeypot(script_name):
    """Starts a honeypot script as a subprocess."""
    try:
        process = subprocess.Popen([sys.executable, script_name], cwd=os.getcwd()) # Run in current directory
        processes.append(process)
        print(f"Started {script_name}")
    except FileNotFoundError:
        print(f"Error: {script_name} not found.")
    except Exception as e:
        print(f"Error starting {script_name}: {e}")


def signal_handler(sig, frame):
    """Handles SIGINT (Ctrl+C) to gracefully stop honeypots."""
    print("\nStopping honeypots...")
    for process in processes:
        try:
            process.send_signal(signal.SIGTERM)  # Send SIGTERM for graceful shutdown
            process.wait(timeout=5)  # Wait for a short period
        except subprocess.TimeoutExpired:
            print(f"Forcefully terminating {process.pid}")  # Might need to be more specific about the script
            process.kill() # Force kill if it doesn't terminate within the timeout
    sys.exit(0)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) # Register the signal handler

    start_honeypot("ftp.py")
    start_honeypot("http_honeypot.py")
    start_honeypot("mysql_honeypot.py")
    start_honeypot("ssh.py")
    start_honeypot("cowrie.py")


    try:
        while True:  # Use a loop to prevent the main process from exiting immediately
            signal.pause()  # Wait for a signal (like SIGINT or SIGTERM)
    except KeyboardInterrupt:
        pass # signal handler takes care of the cleanup

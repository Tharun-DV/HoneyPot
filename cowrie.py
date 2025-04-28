import subprocess

def run_cowrie_docker():
    """Runs the Cowrie honeypot Docker container."""
    try:
        process = subprocess.Popen(
            ["docker", "run", "-p", "22:2222", "cowrie/cowrie:latest"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Important for handling text output
        )

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Cowrie Docker container started successfully.")
            print("Output:")
            print(stdout)

        else:
            print("Error starting Cowrie Docker container.")
            print("Error (stderr):")
            print(stderr)
            print("Return code:", process.returncode)

    except FileNotFoundError:
        print("Error: Docker not found. Make sure Docker is installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_cowrie_docker()

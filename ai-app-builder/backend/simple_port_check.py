import socket
import sys

def check_port(host, port):
    """Check if a port is open on a given host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)  # 3 second timeout
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port {port}: {e}")
        return False

def main():
    # Check common ports
    ports_to_check = [8000, 3000, 3001, 5000, 8080]
    host = "127.0.0.1"
    
    print("Checking if common development ports are in use:")
    print("=" * 50)
    
    for port in ports_to_check:
        is_open = check_port(host, port)
        status = "OPEN" if is_open else "CLOSED"
        print(f"Port {port}: {status}")
    
    print("\nIf port 8000 shows as CLOSED, the server should be able to start.")
    print("If port 8000 shows as OPEN, there might be another process using it.")

if __name__ == "__main__":
    main()
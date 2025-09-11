import socket
import psutil
import sys

def check_port_in_use(port):
    """Check if a port is in use"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

def find_process_using_port(port):
    """Find which process is using a specific port"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    return proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def main():
    port = 8000
    print(f"Checking if port {port} is in use...")
    
    if check_port_in_use(port):
        print(f"Port {port} is currently in use")
        process = find_process_using_port(port)
        if process:
            print(f"Process using port {port}:")
            print(f"  PID: {process['pid']}")
            print(f"  Name: {process['name']}")
        else:
            print("Could not identify process using the port")
    else:
        print(f"Port {port} is not in use")
    
    # Also check common alternative ports
    alt_ports = [3000, 3001, 5000, 8080]
    print(f"\nChecking alternative ports: {alt_ports}")
    for alt_port in alt_ports:
        if check_port_in_use(alt_port):
            print(f"Port {alt_port} is in use")
            process = find_process_using_port(alt_port)
            if process:
                print(f"  Process: {process['name']} (PID: {process['pid']})")

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("psutil not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    main()
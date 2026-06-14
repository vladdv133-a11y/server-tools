import http.server
import socketserver
import socket
import os
import sys
from datetime import datetime

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class CustomTerminalHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for clean terminal logging and UTF-8 filename support."""
    
    def log_message(self, format, *args):
        """Overrides standard stderr logging to output clean, structured CLI logs."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # args[1] is typically the HTTP status code (e.g., 200, 404)
        status = args[1] if len(args) > 1 else "???"
        
        if status == "200" or str(status).startswith("2"):
            status_color = "[ OK ]"
        elif str(status).startswith("3"):
            status_color = "[3XX ]"
        else:
            status_color = "[FAIL]"
            
        sys.stdout.write(f"\r{current_time} {status_color} - {args[0]}\n")
        sys.stdout.flush()

    def list_directory(self, path):
        """Forces UTF-8 configuration to prevent broken characters in terminal/browser."""
        self.extensions_map.update({'': 'text/html; charset=utf-8'})
        return super().list_directory(path)

def start_server(target_dir, port=8080):
    if not os.path.exists(target_dir):
        sys.stderr.write(f"[-] Error: Directory '{target_dir}' not found.\n")
        sys.exit(1)

    os.chdir(target_dir)
    local_ip = get_local_ip()
    
    # Auto-port shifting if port is blocked
    while True:
        try:
            server = socketserver.TCPServer(("", port), CustomTerminalHandler)
            break
        except OSError as e:
            if e.errno in [98, 10048]:
                port += 1
            else:
                sys.stderr.write(f"[-] Socket Bind Error: {e}\n")
                sys.exit(1)

    # Clean Terminal UI Banner
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 65)
    print(f" NET-SHARE CLI SERVER v1.2.0")
    print("=" * 65)
    print(f" [*] STATUS     : RUNNING")
    print(f" [*] PATH       : {os.getcwd()}")
    print(f" [*] LOCAL LINK : http://127.0.0.1:{port}")
    print(f" [*] WIFI LINK  : http://{local_ip}:{port}")
    print("=" * 65)
    print(" [!] Press CTRL+C to kill the process safely.\n")
    print("[LOGS] System active. Monitoring requests...")

    try:
        with server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[-] Halt signal received.")
        print("[*] Closing sockets...")
        print("[+] Server stopped successfully. Core freed.")
        sys.exit(0)

if __name__ == "__main__":
    # If a path argument is passed via terminal (`python server.py C:\Users`), use it.
    # Otherwise, fallback to prompt input.
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        path = input("Enter target directory path (Leave empty for current folder): ").strip().strip('"')
    
    if not path:
        path = "."
        
    start_server(path)
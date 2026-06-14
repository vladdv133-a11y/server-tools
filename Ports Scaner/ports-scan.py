import socket

def check_port(target, port):
    # Creating a socket to attempt a connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    result = s.connect_ex((target, port))
    s.close()
    
    if result == 0:
        # Port is open - applying analysis logic
        print(f"[!] WARNING! Port {port} is OPEN on {target}")
        
        if port == 21 or port == 22:
            print(">>> Status: Port cracked/Insecure access attempt!")
        elif port == 80 or port == 443:
            print(">>> Status: Possible DDoS attack vector or Web vulnerability!")
        else:
            print(">>> Status: Port open, potential risk detected!")
        return True
    return False

if __name__ == "__main__":
    target = input("Enter IP to scan: ")
    # List of critical ports to check
    ports_to_check = [21, 22, 23, 80, 443, 3306, 8080]
    
    print(f"[*] Starting scan for target: {target}...")
    for port in ports_to_check:
        check_port(target, port)
        
    print("\n[!] Scan completed.")
    input("Press Enter to exit...")
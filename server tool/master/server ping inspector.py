import os
import sys
import time
import socket
import subprocess
import requests
from datetime import datetime

def get_ip_from_domain(domain):
    """Converts a domain name (like google.com) into an IP address."""
    try:
        # Прибираємо http:// або https://, якщо користувач ввів їх випадково
        clean_domain = domain.replace("https://", "").replace("http://", "").split('/')[0]
        ip = socket.gethostbyname(clean_domain)
        return ip
    except socket.gaierror:
        return None

def ping_host(host):
    """Pings the target host and returns latency in ms."""
    try:
        output = subprocess.check_output(f"ping -n 1 {host}", shell=True, text=True, encoding='cp866')
        for line in output.split('\n'):
            if "time=" in line or "время=" in line:
                parts = line.split()
                for part in parts:
                    if "time=" in part or "время=" in part:
                        time_ms = part.split('=')[1].replace('ms', '').replace('мс', '')
                        return int(time_ms)
    except Exception:
        return None
    return None

def check_share_server(ip, port=8080):
    """Checks if our Net-Share file server is running on the target IP."""
    try:
        # Спробуємо зробити швидкий запит на вказаний порт
        url = f"http://{ip}:{port}"
        response = requests.get(url, timeout=2)
        
        # Якщо сервер відповів і в тексті сторінки є наш фірмовий заголовок
        if response.status_code == 200 and "NET-SHARE" in response.text:
            return f"ACTIVE SHARE FOUND! -> {url}"
        else:
            return "No files / Standard web server"
    except requests.exceptions.RequestException:
        return "No files / Server offline"

def scan_target(target_input):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print(f" 🔍 NET-TARGET SCANNER v1.0.0 | {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    print(f" [*] Resolving target : {target_input}...")
    ip_address = get_ip_from_domain(target_input)
    
    if not ip_address:
        print(f" [❌] ERROR: Could not resolve domain or invalid IP: '{target_input}'")
        print("=" * 60)
        return

    print(f" [+] Resolved IP      : {ip_address}")
    
    # 1. Перевірка пінгу
    print(f" [*] Testing latency (Ping)...")
    latency = ping_host(ip_address)
    if latency is not None:
        bars = "█" * min(int(latency / 10) + 1, 20)
        print(f" [+] Ping Latency     : {latency} ms {bars}")
    else:
        print(f" [⚠️] Ping Latency     : PACKET LOSS (No response)")

    print("-" * 60)
    
    # 2. Перевірка наявності роздачі файлів (на порту 8080)
    print(f" [*] Scanning for active file sharing (Port 8080)...")
    share_status = check_share_server(ip_address, port=8080)
    print(f" [🎯] Share Status    : {share_status}")
    
    print("=" * 60)
    print("\n [!] Execution finished. Press Enter to scan another target or CTRL+C to exit.")
    input()

if __name__ == "__main__":
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- CLI Target & Share Scanner ---")
            user_target = input("Enter website domain or IP address to scan: ").strip()
            
            if user_target:
                scan_target(user_target)
            else:
                print("[-] Empty input. Please try again.")
                time.sleep(1.5)
    except KeyboardInterrupt:
        print("\n[-] Scanner closed. Terminal freed.")
        sys.exit(0)
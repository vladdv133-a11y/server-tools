import socket

def get_ip_from_domain(domain):
    try:
        # Очищуємо домен від протоколів та шляхів
        clean_domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        ip = socket.gethostbyname(clean_domain)
        return ip
    except socket.gaierror:
        return None

if __name__ == "__main__":
    print("=== IP Resolver ===")
    domain = input("Enter website domain (e.g., google.com): ")
    
    target_ip = get_ip_from_domain(domain)
    
    if target_ip:
        print(f"\n[+] The IP address of {domain} is: {target_ip}")
    else:
        print("\n[!] Error: Could not resolve domain to IP.")
        
    print("-" * 20)
    
    # Цикл очікування виходу
    while True:
        choice = input("Enter Q to Exit: ").strip().upper()
        if choice == 'Q':
            break
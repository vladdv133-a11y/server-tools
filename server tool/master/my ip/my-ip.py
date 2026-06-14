import socket
import requests

# Отримуємо локальну IP
local_ip = socket.gethostbyname(socket.gethostname())

# Отримуємо публічну IP
try:
    public_ip = requests.get('https://api.ipify.org').text
except:
    public_ip = "Offline"

print(f"local: {local_ip}")
print(f"public: {public_ip}")

input("\nclick Q to quit...")
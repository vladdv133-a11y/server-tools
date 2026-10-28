import socket
import requests

local_ip = socket.gethostbyname(socket.gethostname())

try:
    public_ip = requests.get('https://api.ipify.org').text
except:
    public_ip = "Offline"

print(f"local: {local_ip}")
print(f"public: {public_ip}")

input("\nclick Q to quit...")

import subprocess
import time
import platform

def get_wifi_strength():
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '8.8.8.8']
    
    start = time.perf_counter()
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    
    latency = (end - start) * 1000
    strength = max(0, min(100, 100 - (latency * 2)))
    return round(strength, 2), round(latency, 2)

print("=================")
print (" wifi speed test")
print("=================")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        strength, latency = get_wifi_strength()
        print(f"Signal: {strength}% | Latency: {latency}ms", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nTest stopped by user.")

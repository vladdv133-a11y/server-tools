import requests
import time

def check_website():
    print("====================================")
    print("         SITE CHECK REQUEST         ")
    print("====================================")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = input("Enter website URL (e.g., https://google.com): ")
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\nMonitoring {url}...")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] {url} is UP. Status Code: {response.status_code}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] {url} returned Status Code: {response.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] {url} is DOWN. Error: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    check_website()
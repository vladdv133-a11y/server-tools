import subprocess
import re

def get_all_wifi_data():
    print("\n--- [WiFi Data & Network Scanner] ---")
    
    try:
        profiles_raw = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding='cp866')
        profiles = re.findall(r"All User Profile\s+:\s+(.*)", profiles_raw)
    except Exception as e:
        print(f"[!] Error: {e}")
        return

    try:
        addr_info = subprocess.check_output(["netsh", "interface", "ip", "show", "addresses"], encoding='cp866')
    except:
        addr_info = ""

    for profile in profiles:
        profile = profile.strip()
        cmd = ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='cp866')
        
        print(f"\nNetwork: {profile}")
        
        match = re.search(r"Key Content\s+:\s+(.*)", result.stdout)
        print(f"Code: {match.group(1) if match else 'Not available'}")

        interface_check = subprocess.run(["netsh", "wlan", "show", "interface"], capture_output=True, text=True, encoding='cp866')
        
        if profile in interface_check.stdout:
            ip_match = re.search(r"IP Address:\s+([\d\.]+)", addr_info)
            print(f"[+] Status: Active | IP: {ip_match.group(1) if ip_match else 'Connected (No IP)'}")
        else:
            print("Status: Saved (Not currently connected)")
            
        print("-" * 40)

if __name__ == "__main__":
    get_all_wifi_data()
    input("\nPress Enter to exit...")
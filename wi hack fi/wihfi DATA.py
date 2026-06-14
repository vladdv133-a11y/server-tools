import subprocess
import re

def get_all_wifi_data():
    print("\n--- [WiFi Data Scanner - Automatic Mode] ---")
    
    # 1. Отримуємо список усіх збережених профілів WiFi
    try:
        # Команда отримує список усіх мереж
        profiles_raw = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding='cp866')
        # Використовуємо регулярні вирази, щоб витягнути назви всіх мереж зі списку
        profiles = re.findall(r"All User Profile     : (.*)", profiles_raw)
    except Exception as e:
        print(f"[!] Error: {e}")
        return

    if not profiles:
        print("[!] No WiFi profiles found.")
        return

    print(f"[*] Found {len(profiles)} networks. Analyzing codes...\n")

    # 2. Проходимо циклом по кожній знайденій мережі
    for profile in profiles:
        profile = profile.strip()
        # Команда для отримання деталей конкретної мережі (з ключем безпеки)
        cmd = ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='cp866')
        
        # 3. Виводимо інформацію про мережу
        print(f"Network: {profile}")
        
        # Витягуємо "Key Content" (це і є код/пароль) за допомогою регулярного виразу
        match = re.search(r"Key Content            : (.*)", result.stdout)
        if match:
            print(f"Code: {match.group(1)}")
        else:
            print("Code: Not available (Open network or hidden)")
        print("-" * 40)

if __name__ == "__main__":
    # Важливо: обов'язково запускай від імені Адміністратора!
    get_all_wifi_data()
    input("\nPress Enter to exit...")
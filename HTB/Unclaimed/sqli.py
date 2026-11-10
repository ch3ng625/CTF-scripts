import requests
import json
from colorama import Fore, Style

url = "http://unclaimed.htb/ask"

def main():
    while True:
        print(Fore.BLUE + "[*] SQL query: (enter 'exit' to quit)" + Style.RESET_ALL)
        query = input(Fore.BLUE + ">> " + Style.RESET_ALL)
        if query == "exit":
            print(Fore.YELLOW + "[-] Bye" + Style.RESET_ALL)
            break
        
        data = {
            "msg": f"HTB-OPS-4471 {query}"
        }

        try:
            r = requests.post(url, json=data)
        except requests.RequestException as e:
            print(Fore.RED + f"[-] Something went wrong.")
            print(f"[-] Error: {e}" + Style.RESET_ALL)
            exit(0)
        
        if r.status_code != 200:
            print(Fore.RED + f"[-] Unknown status code: {r.status_code}." + Style.RESET_ALL)
            print(Fore.RED + f"[-] {r.text}" + Style.RESET_ALL)
            exit(0)
        
        response = json.loads(r.text)
        print(response["reply"])

    return

if __name__ == "__main__":
    main()
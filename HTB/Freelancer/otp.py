import cv2
from pyzbar import pyzbar
import requests
from bs4 import BeautifulSoup
import sys
from PIL import Image
from io import BytesIO
import numpy as np
import base64
from colorama import Fore, Style

base_url = "http://freelancer.htb"

def get_csrftokens():
	url = f"{base_url}/accounts/login/"
	try:
		r = requests.get(url)
	except requests.RequestException as e:
		print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	csrftoken = r.cookies['csrftoken']
	print(Fore.BLUE + f"[*] CSRF cookie: {csrftoken}" + Style.RESET_ALL)

	soup = BeautifulSoup(r.text, 'html.parser')
	csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
	print(Fore.BLUE + f"[*] CSRF middleware token: {csrfmiddlewaretoken}" + Style.RESET_ALL)

	return (csrftoken, csrfmiddlewaretoken)

def login(username, password, csrftoken, csrfmiddlewaretoken):
	url = f"{base_url}/accounts/login/"
	cookies = {"csrftoken": csrftoken}
	data = {"csrfmiddlewaretoken": csrfmiddlewaretoken,
			"username": username,
			"password": password}

	try:
		r = requests.post(url, data=data, cookies=cookies, allow_redirects=False)
	except requests.RequestException as e:
		print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	if r.status_code == 200:
		print(Fore.RED + "[-] Login failed." + Style.RESET_ALL)
		exit(0)

	if r.status_code == 403:
		print(Fore.RED + "[-] Invalid CSRF token." + Style.RESET_ALL)
		exit(0)

	if r.status_code != 302:
		print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
		exit(0)

	sessionid = r.cookies['sessionid']

	print(Fore.BLUE + "[+] Login successful." + Style.RESET_ALL)
	print(Fore.BLUE + f"[*] Session cookie: {sessionid}" + Style.RESET_ALL)
	return sessionid

def get_otp(sessionid):
	url = f"{base_url}/accounts/otp/qrcode/generate/"
	cookies = {"sessionid": sessionid}

	try:
		r = requests.get(url, cookies=cookies)
	except r.RequestException as e:
		print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
		print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
		exit(0)

	img_array = np.array(bytearray(r.content), dtype=np.uint8)
	img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

	qr = pyzbar.decode(img)

	otp_url = qr[0].data.decode('utf-8')
	print(Fore.GREEN + "[+] OTP successfully generated." + Style.RESET_ALL)
	print(Fore.GREEN + f"[+] Link: {otp_url}" + Style.RESET_ALL)

	otp = otp_url.split('/')[-2]
	print(Fore.GREEN + f"[*] OTP: {otp}" + Style.RESET_ALL)

	return

def main():
	if len(sys.argv) != 3:
		print("Usage: python otp.py <username> <password>")

		exit(0)

	username = sys.argv[1]
	password = sys.argv[2]

	(csrftoken, csrfmiddlewaretoken) = get_csrftokens()

	sessionid = login(username, password, csrftoken, csrfmiddlewaretoken)

	get_otp(sessionid)

	return

if __name__ == "__main__":
	main()

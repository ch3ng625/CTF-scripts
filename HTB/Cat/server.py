from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode('utf-8')

		print(f"[+] Received POST request:")
		print(f"{post_data}")

		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(b"Received")

PORT = 8000
server_address = ('', PORT)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

print(f"[*] Listening on port {PORT}...")
httpd.serve_forever()

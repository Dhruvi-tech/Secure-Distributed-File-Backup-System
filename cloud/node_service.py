from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Node service running")

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Starting node service on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

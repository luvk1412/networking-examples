from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        print(f'INIT{self.path if hasattr(self, "path") else "None"}')
        self.id = random.randint(1, 10000)
        print(f"[{self.id}] New connection established...")
        super().__init__(*args, **kwargs)

    def handle(self):
        print(f'HandlePath{self.path if hasattr(self, "path") else "None"}')
        print(f"[{self.id}] Start of request received...")
        super().handle()

    def do_POST(self):
        # Indicate that headers are being received
        print(f"[{self.id}] Receiving headers...")

        # Print all headers
        headers = self.headers
        for h in headers:
            print(f"[{self.id}] {h}: {headers[h]}")

        # Indicate that header reception is complete
        print(f"[{self.id}] Headers received.")

        # Read the content length, if provided
        content_length = int(self.headers.get('Content-Length', 0))

        # Read the body data
        body = self.rfile.read(content_length).decode('utf-8') if content_length else ''
        print(f"[{self.id}] Body received: {body}")

        # Send response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": f"OK {self.id}"}
        self.wfile.write(json.dumps(response).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

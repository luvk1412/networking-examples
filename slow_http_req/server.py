import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random


class EchoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.id = random.randint(1, 10000)
        print(f"[{self.id}] New connection established...")
        super().__init__(*args, **kwargs)

    def handle(self):
        # Record that handling of the request has started
        print(f"[{self.id}] Start of request received...")
        super().handle()

    def handle_request(self):
        # Timestamp when headers are fully received
        self.headers_received_time = time.time()
        print(f"[{self.id}] Headers received at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.headers_received_time))}")

        # Read the body if any
        content_length = self.headers.get('Content-Length')
        post_data = None
        if content_length:
            content_length = int(content_length)
            post_data = self.rfile.read(content_length).decode('utf-8')
            body_received_time = time.time()
            print(f"[{self.id}] Body received at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(body_received_time))}")

        # Prepare response data
        response_data = {
            'method': self.command,
            'path': self.path,
            'headers': dict(self.headers),
            'body': post_data
        }

        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

        # Timestamp when response is sent
        self.response_sent_time = time.time()
        print(f"[{self.id}] Response sent at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.response_sent_time))}")

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_HEAD(self):
        self.handle_request()


def run(server_class=HTTPServer, handler_class=EchoHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

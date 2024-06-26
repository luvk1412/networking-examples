import socket
import time


def send_request_char_by_char(host, port, headers, body, delay=0.5):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((host, port))
        print("Starting headers send")
        time.sleep(5)

        # Send the HTTP request character by character
        for char in headers:
            sock.send(char.encode('utf-8'))  # Send each character
            print(f"Sent: {char}")
            time.sleep(delay)  # Sleep after sending each character
        print("Sent headers")
        sock.send("\r\n".encode('utf-8'))
        time.sleep(5)
        print("Started sending body")
        for char in body:
            sock.send(char.encode('utf-8'))  # Send each character
            print(f"Sent: {char}")
            time.sleep(delay)  # Sleep after sending each character
        print("Sent Body")

        # Wait for the response (this part does not handle the response char by char)
        response = sock.recv(4096)
        print("Response from the server:")
        print(response.decode('utf-8'))


if __name__ == "__main__":
    host = 'localhost'
    port = 8888

    # Prepare the POST request
    body = "This is a test data\r\n"
    headers_lines = [
        "POST /service1/post  HTTP/1.1",
        "Host: localhost",
        "Content-Type: text/plain",
        "x-session-token: token1",
        f"Content-Length: {len(body)}",
    ]

    # Combine the request lines and make sure to use CRLF (\r\n) for HTTP protocol compliance
    header_str = "\r\n".join(headers_lines) + "\r\n"

    # Send the request character by character
    send_request_char_by_char(host, port, header_str, body, delay=0.1)  # Adjust delay as needed

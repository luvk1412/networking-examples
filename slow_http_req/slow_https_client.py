import socket
import ssl
import time


def send_request_char_by_char(host, port, headers, body, delay=0.5):
    # Create a socket object and wrap it with SSL for HTTPS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            print("Starting headers send")
            time.sleep(1)

            # Send the HTTP request headers character by character
            for char in headers:
                ssock.send(char.encode('utf-8'))  # Send each character securely over SSL
                print(f"Sent: {char}")
                time.sleep(delay)  # Sleep after sending each character
            print("Sent headers")
            ssock.send("\r\n".encode('utf-8'))  # Ensure to end headers properly
            print("Started sending body")
            time.sleep(1)

            # Send the body character by character
            for char in body:
                ssock.send(char.encode('utf-8'))  # Send each character securely over SSL
                print(f"Sent: {char}")
                time.sleep(delay)  # Sleep after sending each character
            print("Sent Body")

            # Wait for the response (this part does not handle the response char by char)
            response = ssock.recv(4096)
            print("Response from the server:")
            print(response.decode('utf-8'))


if __name__ == "__main__":
    host = 'flockmail-backend.flock-staging.com'
    port = 443  # SSL port for HTTPS

    # Prepare the POST request
    body = "This is a test data\r\n"
    headers_lines = [
        "POST /ggserver/s HTTP/1.1",
        "Host: flockmail-backend.flock-staging.com",
        "Content-Type: text/plain",
        f"Content-Length: {len(body)}",
    ]
    # Combine the request lines and make sure to use CRLF (\r\n) for HTTP protocol compliance
    header_str = "\r\n".join(headers_lines) + "\r\n"

    # Send the request character by character
    send_request_char_by_char(host, port, header_str, body, delay=0.1)  # Adjust delay as needed

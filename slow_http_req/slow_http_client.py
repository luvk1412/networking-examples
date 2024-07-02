import socket
import time

batch_size = 1024 * 1024

def send_request_char_by_char(host, port, headers, body, delay=0.5):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)  # Buffer size 1024
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)  # Buffer size 1024
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
        response_parts = []
        batch_ct = 0
        total_size_read = 0
        while True:
            batch = sock.recv(batch_size)  # Adjust the size of each batch
            if not batch:
                break  # If no more data is received, exit the loop
            batch_ct += 1
            decoded_batch = batch.decode("utf-8")

            total_size_read += len(decoded_batch)
            response_parts.append(batch)
            print(f'Read total {total_size_read} bytes in {batch_ct} batches. data: "{decoded_batch[:10]}", len.data: "{len(decoded_batch)}"')
            time.sleep(0.01)
            if decoded_batch.endswith("0\r\n\r\n"):
                break

        # Combine all parts into the final response
        response = b''.join(response_parts).decode('utf-8')
        print("Complete response from the server:")
        print(response[:800] + ' ... ' + response[-20:])


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
        "x-resp-mb: 1",
        f"Content-Length: {len(body)}",
    ]

    # Combine the request lines and make sure to use CRLF (\r\n) for HTTP protocol compliance
    header_str = "\r\n".join(headers_lines) + "\r\n"

    # Send the request character by character
    send_request_char_by_char(host, port, header_str, body, delay=0.1)  # Adjust delay as needed

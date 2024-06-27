import socket
import ssl
import time

batch_size = 10

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
            response_parts = []
            batch_ct = 0
            total_size_read = 0
            while True:
                batch = ssock.recv(batch_size)  # Adjust the size of each batch
                if not batch:
                    break  # If no more data is received, exit the loop
                batch_ct += 1
                decoded_batch = batch.decode("utf-8")

                total_size_read += len(decoded_batch)
                response_parts.append(batch)
                print(f'Read total {total_size_read} bytes in {batch_ct} batches. data: "{decoded_batch[:10]}", len.data: "{len(decoded_batch)}"')
                time.sleep(0.1)
                if decoded_batch == "0\r\n\r\n":
                    break

            # Combine all parts into the final response
            response = b''.join(response_parts).decode('utf-8')
            print("Complete response from the server:")
            print(response[:500])


if __name__ == "__main__":
    host = 'flockmail-backend.flock-staging.com'
    port = 443  # SSL port for HTTPS

    # Prepare the POST request
    body = "This is a test data\r\n"
    headers_lines = [
        "POST /ggserver/s HTTP/1.1",
        "Host: flockmail-backend.flock-staging.com",
        "Content-Type: text/plain",
        "x-resp-mb: 3",
        f"Content-Length: {len(body)}",
    ]
    # Combine the request lines and make sure to use CRLF (\r\n) for HTTP protocol compliance
    header_str = "\r\n".join(headers_lines) + "\r\n"

    # Send the request character by character
    send_request_char_by_char(host, port, header_str, body, delay=0.1)  # Adjust delay as needed

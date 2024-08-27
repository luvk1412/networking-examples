import socket
import time
import concurrent.futures

batch_size = 1024 * 1024


def send_request_char_by_char(host, port, headers, body, delay=0.5, request_id=0):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)  # Buffer size 1024
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)  # Buffer size 1024

            # Connect to the server
            print(f"Request {request_id}: Connecting to {host}:{port}")
            sock.connect((host, port))
            print(f"Request {request_id}: Connected to the server")

            print(f"Request {request_id}: Starting headers send")
            time.sleep(5)

            # Send the HTTP request character by character
            for char in headers:
                sock.send(char.encode('utf-8'))  # Send each character
                print(f"Request {request_id}: Sent: {char}")
                time.sleep(delay)  # Sleep after sending each character

            print(f"Request {request_id}: Sent headers")
            sock.send("\r\n".encode('utf-8'))
            time.sleep(5)
            print(f"Request {request_id}: Started sending body")
            chars_sent = 0
            body_len = len(body)
            for char in body:
                sock.send(char.encode('utf-8'))  # Send each character
                chars_sent += 1
                if body_len - chars_sent < 20:  # For large bodies during testing only add sleep/ during last few bytes
                    print(f"Request {request_id}: Sent: {char}")
                    time.sleep(delay)  # Sleep after sending each character
                if chars_sent % 100_000 == 0:
                    print(f"Request {request_id}: Sent: {chars_sent} chars")

                # if body_len - 2 == chars_sent:
                #     print(f"Request {request_id}: Stopping body sending")
                #     time.sleep(10)

            print(f"Request {request_id}: Sent Body")

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
                print(f'Request {request_id}: Read total {total_size_read} bytes in {batch_ct} batches. data: "{decoded_batch[:10]}", len.data: "{len(decoded_batch)}"')
                time.sleep(0.01)
                if decoded_batch.endswith("0\r\n\r\n"):
                    break

            # Combine all parts into the final response
            response = b''.join(response_parts).decode('utf-8')
            print(f"Request {request_id}: Complete response from the server:")
            print(response[:800] + ' ... ' + response[-20:])
    except Exception as e:
        print(f"Request {request_id}: An error occurred - {e}")


if __name__ == "__main__":
    host = 'localhost'
    port = 8888

    # Prepare the POST request
    extra_body_size = 0
    body = "a" * extra_body_size + "This is a test data\r\n"
    headers_lines = [
        "POST /service1/post  HTTP/1.1",
        "Host: localhost",
        "Content-Type: text/plain",
        "x-session-token: token1",
        # "x-resp-mb: 1",
        f"Content-Length: {len(body)}",
    ]

    # Combine the request lines and make sure to use CRLF (\r\n) for HTTP protocol compliance
    header_str = "\r\n".join(headers_lines) + "\r\n"

    # Send the request character by character
    # send_request_char_by_char(host, port, header_str, body, delay=0.1)  # Adjust delay as needed
    num_requests = 1
    delay = 0.1
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [
            executor.submit(send_request_char_by_char, host, port, header_str, body, delay, request_id)
            for request_id in range(1, num_requests + 1)
        ]
        concurrent.futures.wait(futures)

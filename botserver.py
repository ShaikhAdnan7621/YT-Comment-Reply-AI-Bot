import socket
import threading
from ytbot.commentmodel import get_comment_reply

def start_server(stop_event, host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        s.settimeout(1.0)  # allow periodic check for stop_event
        print(f"Server listening on {host}:{port}")
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()  # attempt to accept a connection
            except socket.timeout:
                continue
            with conn:
                data = conn.recv(2048)
                if not data:
                    continue
                req = data.decode('utf-8')
                if req.startswith("OPTIONS"):
                    resp = (
                        "HTTP/1.1 200 OK\r\n"
                        "Access-Control-Allow-Origin: *\r\n"
                        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
                        "Access-Control-Allow-Headers: Content-Type\r\n"
                        "Content-Length: 0\r\n\r\n"
                    )
                else:
                    comment_text = req.split("\r\n\r\n", 1)[1].strip() if "\r\n\r\n" in req else req.strip()
                    reply = get_comment_reply(comment_text)
                    response_body = reply
                    resp = (
                        "HTTP/1.1 200 OK\r\n"
                        "Access-Control-Allow-Origin: *\r\n"
                        "Content-Type: text/plain; charset=utf-8\r\n"
                        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n"
                        + response_body
                    )
                conn.sendall(resp.encode('utf-8'))
        print("Server stopped.")

if __name__ == '__main__':
    stop_event = threading.Event()
    server_thread = threading.Thread(target=start_server, args=(stop_event,), daemon=True)
    server_thread.start()
    
    while True:
        user_input = input("Type 'stop' or 'close' to stop the server...\n")
        if user_input.lower() in ['stop', 'close']:
            break
        print("Invalid command. Please type 'stop' or 'close'.")
    
    stop_event.set()
    server_thread.join()

import socket
import sys

from ..utils import read_from_socket, send_message


PORT = 9291


def parse_args():
    global PORT
    if len(sys.argv) >= 2:
        PORT = sys.argv[1]


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", PORT))
    sock.listen(5)

    proxy_socket, address = sock.accept()
    print(f"Make proxy agent connection {address}")

    try:
        while True:
            new_request_socket, adress = sock.accept()
            request: bytearray = read_from_socket(new_request_socket)
            print(f"Get user request from {adress}")
            send_message(proxy_socket, request)
            print(f"Pass request - {request}")
            response: bytes = read_from_socket(proxy_socket)
            print(f"Got response - {response}")
            send_message(new_request_socket, response)
            new_request_socket.close()
    except BaseException as err:
        print(f"Finished because {err}")
        new_request_socket.close()
        sock.close()
        proxy_socket.close()


if __name__ == '__main__':
    main()

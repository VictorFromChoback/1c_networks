import socket
import sys

from ..utils import read_from_socket, send_message


PROXY_PORT, PORT = 9291, 9295


def parse_args():
    global PROXY_PORT, PORT
    if len(sys.argv) >= 2:
        PROXY_PORT = sys.argv[1]
    if len(sys.argv) >= 3:
        PORT = sys.argv[2]


def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind(("localhost", PORT))
        client.connect(("localhost", PROXY_PORT))
        msg = b'Give some data'
        send_message(client, bytearray(msg), protocol=True, proxy=True)
        print(read_from_socket(client).decode())
    except BaseException as err:
        print(err)
    client.close()


if __name__ == '__main__':
    main()

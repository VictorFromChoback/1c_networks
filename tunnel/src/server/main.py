import socket
import sys

from ..utils import read_from_socket, send_message


PORT = 9290


def parse_args():
    global PORT
    if len(sys.argv) >= 2:
        PORT = sys.argv[1]


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", PORT))
    sock.listen(5)
    try:
        while True:
            connection, _ = sock.accept()
            _: bytes = read_from_socket(connection)
            print("New request !!!")
            send_message(connection, bytes("This is simple response", "utf8"), protocol=True)
            connection.close()
    except BaseException as err:
        print(f"Finished because {err}")
        connection.close()
        sock.close()


if __name__ == '__main__':
    main()

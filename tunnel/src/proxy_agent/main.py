import socket
import sys

from ..utils import read_from_socket, send_message


SERVER_PORT, PROXY_PORT, CLIENT_PORT, PROXY_CLIENT_PORT = 9290, 9291, 9292, 9293


def parse_args():
    global SERVER_PORT, PROXY_PORT, CLIENT_PORT, PROXY_CLIENT_PORT
    if len(sys.argv) >= 2:
        SERVER_PORT = sys.argv[1]
    if len(sys.argv) >= 3:
        PROXY_PORT = sys.argv[2]
    if len(sys.argv) >= 4:
        CLIENT_PORT = sys.argv[3]
    if len(sys.argv) >= 5:
        PROXY_CLIENT_PORT = sys.argv[4]


def main():
    proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_client.bind(("localhost", PROXY_CLIENT_PORT))
    proxy_client.connect(("localhost", PROXY_PORT))

    try:
        while True:
            msg_from_proxy_server: bytes = read_from_socket(proxy_client)
            if not msg_from_proxy_server:
                continue
            print(f"Proxy request received {msg_from_proxy_server} !!!")

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", SERVER_PORT))

            send_message(client, msg_from_proxy_server)
            msg_from_server = read_from_socket(client)
            print(f"Transmit response - {msg_from_server}")
            send_message(proxy_client, msg_from_server)
            client.close()
            print("Tunnel iteration finished")
    except BaseException as err:
        print(f"Finished because {err}")
        client.close()
        proxy_client.close()


if __name__ == '__main__':
    main()

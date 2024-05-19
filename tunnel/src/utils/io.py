import socket


STOP_PROTOCOL_TOKEN = bytes('#STOPAVPCL', 'utf8')
STOP_PROXY_TOKEN = bytes('#STOPPROXY', 'utf8')
HTTP_TOKEN = b'\r\n\r\n'
CONTENT_LENGTH = 'Content-Length'


def is_stop_protocol(msg: bytearray) -> bool:
    return msg[-len(STOP_PROTOCOL_TOKEN):] == STOP_PROTOCOL_TOKEN


def is_stop_proxy(msg: bytearray) -> bool:
    return msg[-len(STOP_PROXY_TOKEN):] == STOP_PROXY_TOKEN


def extract_size(msg: str, j: int) -> int:
    size_str = ""
    while msg[j] != '\r':
        size_str += msg[j]
        j += 1
    return int(size_str)


def is_http(msg: bytearray) -> bool:
    text_msg = msg.decode()
    j = text_msg.find(CONTENT_LENGTH)
    if j != -1:
        size = extract_size(text_msg, j + len(CONTENT_LENGTH) + 2)
        i = msg.find(HTTP_TOKEN)
        if i == -1:
            return False
        print(size, i, len(msg) - i - len(HTTP_TOKEN))
        if len(msg) - i - len(HTTP_TOKEN) == size:
            return True
    else:
        return msg[-len(HTTP_TOKEN):] == HTTP_TOKEN
    return False


def clip_msg(msg: bytearray, protocol: bool = False, proxy: bool = False):
    if protocol:
        return msg[:-len(STOP_PROTOCOL_TOKEN)]
    if proxy:
        return msg[:-len(STOP_PROXY_TOKEN)]
    return msg


def send_message(socket: socket.socket,
                 msg: bytearray,
                 protocol: bool = False,
                 proxy: bool = False) -> None:
    msg_with_suffix = bytearray(msg)
    if protocol:
        msg_with_suffix.extend(STOP_PROTOCOL_TOKEN)
    if proxy:
        msg_with_suffix.extend(STOP_PROXY_TOKEN)
    socket.sendall(msg_with_suffix)


def read_from_socket(socket: socket.socket):
    response = bytearray()
    socket.settimeout(10.0)
    try:
        while True:
            msg = socket.recv(1024)
            if not msg:
                break
            response.extend(msg)
            if is_stop_protocol(response):
                break
            if is_stop_proxy(response):
                response = clip_msg(response, proxy=True)
                break
            if is_http(response):
                break
    except TimeoutError:
        pass
    return response

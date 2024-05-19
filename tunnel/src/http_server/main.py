import sys
import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


PORT = 9290


def parse_args():
    global PORT
    if len(sys.argv) >= 2:
        PORT = sys.argv[1]


class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", "148")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
        self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode())

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        req_body = json.loads(self.rfile.read(length))
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", f"{length}")
        self.end_headers()
        self.wfile.write('{'.encode())
        for j, (key, value) in enumerate(req_body.items()):
            self.wfile.write('"'.encode())
            self.wfile.write(value.encode())
            self.wfile.write('":"'.encode())
            self.wfile.write(key.encode())
            self.wfile.write('"'.encode())
            if j != len(req_body) - 1:
                self.wfile.write(','.encode())
        self.wfile.write('}'.encode())
        # self.wfile.write('{"'.encode())
        # self.wfile.write(req_body['key'].encode())
        # self.wfile.write(':"key"}"'.encode())
        # self.wfile.write('{"key":"'.encode())
        # self.wfile.write(req_body['key'].encode())
        # self.wfile.write('"}'.encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == "__main__":
    parse_args()
    run(handler_class=HttpGetHandler)

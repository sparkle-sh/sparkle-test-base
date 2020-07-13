import socket
import struct
import json
import os

CONNECTOR_PORT = 7777
CONNECTOR_HOST = os.getenv("CONNECTOR_HOST", '127.0.0.1')


class ConnectorClient(object):
    def __init__(self, session_type='agent'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_type = session_type

    def connect(self, host=CONNECTOR_HOST, port=CONNECTOR_PORT):
        print("connecting")
        self.sock.settimeout(15)
        self.sock.connect((host, port))

    def disconnect(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except OSError:
            pass

    def get_validated_response(self):
        response = self.get_response()
        assert(response is not None)

        header = response.get("header")
        assert(header is not None)

        content = response.get("content")
        assert(content is not None)

        return header, content

    def send_handshake(self):
        print("sending handshake")
        handshake = {
            "header": "handshake_request",
            "content": {
                "session_type": self.session_type
            }
        }

        self.send_request(handshake)
        header, _ = self.get_validated_response()

        assert(header == "handshake_response")

    def send_request(self, msg):
        payload = json.dumps(msg)
        self.send_raw_request(payload)

    def send_raw_request(self, payload):
        self.sock.sendall(struct.pack("I", len(payload)))
        self.sock.sendall(payload.encode())

    def get_response(self):
        length = struct.unpack("I", self.sock.recv(4))
        response = self.sock.recv(length[0])
        return json.loads(response.decode())

    def __request(self, payload, wait=True, check=True):
        self.send_request(payload)
        if not wait:
            return
        res = self.get_response()
        header = res.get("header")
        content = res.get("content")
        if check:
            assert header == payload.get("header")
        return header, content

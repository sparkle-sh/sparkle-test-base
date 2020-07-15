import socket
import threading
import queue
import json
import struct

from ..config import CONNECTOR_PORT


class FakeConnector(threading.Thread):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True
        self.queue = queue.Queue()

    def run(self):
        self.socket.bind(("127.0.0.1", CONNECTOR_PORT))
        self.socket.listen(5)
        print("listening")
        while self.is_running:
            length = struct.unpack("I", self.socket.recv(4))
            _ = self.socket.recv(length[0])
            payload = json.dumps(self.queue.get())
            self.socket.sendall(struct.pack("I", len(payload)))
            self.socket.sendall(payload.encode())

    def enqueue_response(self, response):
        self.queue.put(response)

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.socket.close()
            self.join()

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
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = True
        self.queue = queue.Queue()
        self.client = None

    def run(self):
        try:
            self.socket.bind(("127.0.0.1", CONNECTOR_PORT))
            self.socket.listen(5)

            self.client, addr = self.socket.accept()
            while self.is_running:
                self.client.recv(1024)
                payload = json.dumps(self.queue.get())
                self.client.sendall(struct.pack("I", len(payload)))
                self.client.sendall(payload.encode())
        except OSError:
            if self.is_running:
                raise

    def enqueue_response(self, response):
        self.queue.put(response)

    def stop(self):
        if self.is_running:
            self.socket.close()
            self.is_running = False
            if self.client:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            self.join()

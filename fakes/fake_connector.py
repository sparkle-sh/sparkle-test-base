import socket
import threading
import queue
import json
import struct


class FakeConnector(threading.Thread):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True
        self.queue = queue.Queue()

    def run(self):
        while self.is_running:
            self.socket.recv(1024)
            payload = json.dumps(self.queue.get())
            self.socket.sendall(struct.pack("I", len(payload)))
            self.socket.sendall(payload.encode())

    def enqueue_response(self, response):
        self.queue.put(response)

    def stop(self):
        self.is_running = False
        self.socket.close()
        self.join()

import socket
import threading
import queue
import json
import struct
import time
import asyncio

from .config import CONNECTOR_PORT


class FakeConnector(threading.Thread):
    def __init__(self):
        print("creating thread")
        super().__init__(daemon=True)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", CONNECTOR_PORT))
        self.socket.listen(5)
        self.is_running = True
        self.queue = queue.Queue()
        self.client = None

    def run(self):
        print("starting")
        try:
            print("waiting for connection")
            self.client, addr = self.socket.accept()
            print("accepted connection")
            while self.is_running:
                print("waiting for request")
                self.client.recv(1024)
                payload = json.dumps(self.queue.get())
                print("sending response")
                self.client.sendall(struct.pack("I", len(payload)))
                self.client.sendall(payload.encode())
        except OSError as e:
            print("error %s" % str(e))
            if self.is_running:
                raise

    def enqueue_response(self, response):
        self.queue.put(response)

    def stop(self):
        time.sleep(1)
        if self.is_running:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.is_running = False
            if self.client:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            self.join()


if __name__ == "__main__":
    f = FakeConnector()
    f.start()
    time.sleep(5)
    f.stop()

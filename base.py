import unittest
import time
import socket
import os
import docker

from base.connector_client import ConnectorClient, CONNECTOR_HOST, CONNECTOR_PORT


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        if os.getenv("SPARKLE_CONNECTOR_TEST_ENV") is not None:
            client = docker.from_env()
            self.container = client.containers.run(
                image='sparkle-connector', entrypoint='./build/bin/sparkle-connector',
                detach=True, ports={'7777/tcp': 7777}, auto_remove=True, name='sparkle-connector'
            )
        self.wait_for_connector()

    def tearDown(self):
        if os.getenv("SPARKLE_CONNECTOR_TEST_ENV") is not None:
            self.container.kill()
            time.sleep(1)
        super().tearDown()

    def wait_for_connector(self, port=CONNECTOR_PORT, host=CONNECTOR_HOST, timeout=15.0):
        start_time = time.perf_counter()
        while True:
            try:
                with socket.create_connection((host, port), timeout=timeout):
                    break
            except OSError as ex:
                time.sleep(0.01)
                if time.perf_counter() - start_time >= timeout:
                    self.fail(
                        'Waited too long for the port {} on host {} to start accepting connections.'.format(port, host))

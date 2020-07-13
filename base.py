import unittest
import time
import socket
import os
import docker

from .config import *


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.modules = []

    def tearDown(self):
        for module in self.modules:
            module.kill()
            time.sleep(1)
        super().tearDown()

    def start_connector(self):
        self.start_container(
            CONNECTOR_DOCKER, entrypoint='./build/bin/sparkle-connector', ports={'7777/tcp': 7777})

    def start_midpoint(self):
        self.start_container(
            MIDPOINT_DOCKER, entrypoint='./bin/spawn.sh', ports={'7778/tcp': 7778})

    def start_api_gateway(self):
        pass

    def start_container(self, image, entrypoint, ports):
        client = docker.from_env()
        container = client.containers.run(
            image=image, entrypoint=entrypoint,
            detach=True, ports=ports, auto_remove=True, name=image
        )
        self.modules.append(container)

    def wait_for_connector(self):
        self.wait_for(CONNECTOR_PORT, CONNECTOR_HOST)

    def wait_for_midpoint(self):
        self.wait_for(MIDPOINT_PORT, MIDPOINT_HOST)

    def wait_for_api_gw(self):
        self.wait_for(API_GW_PORT, API_GW_HOST)

    def wait_for(self, port, host, timeout=15.0):
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

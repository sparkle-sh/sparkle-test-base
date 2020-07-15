import unittest
import time
import socket
import os
import docker
import requests

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

    def is_test_env(self):
        return os.getenv("SPARKLE_TEST_ENV") is not None

    def wrapped_request(self, method, url, **kwargs):
        body = {}
        try:
            res = method("{}{}".format(url), **kwargs)
            if res.headers["content-type"] == 'application/json':
                body = json.loads(res.text)
            return res.status_code, body
        except requests.exceptions.ConnectionError as e:
            self.fail("endpoint provider is down")

    def start_connector(self, local=True):
        self.start_container(
            CONNECTOR_DOCKER, entrypoint='./build/bin/sparkle-connector', ports={'7777/tcp': 7777})

    def start_midpoint(self, local=True):
        self.start_container(
            MIDPOINT_DOCKER, entrypoint='./bin/spawn.sh', ports={'7778/tcp': 7778})

    def start_api_gateway(self, local=True):
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

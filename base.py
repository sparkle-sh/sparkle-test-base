import unittest
import time
import socket
import os
import docker
import json
import requests
import psycopg2
from timeit import default_timer as timer

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
            res = method(url, **kwargs)
            if res.headers["content-type"] == 'application/json':
                body = json.loads(res.text)
            return res.status_code, body
        except requests.exceptions.ConnectionError as e:
            self.fail("endpoint provider is down")

    def start_connector(self, local=False):
        self.start_container(
            CONNECTOR_DOCKER, local, entrypoint='./build/bin/sparkle-connector', ports={f'{CONNECTOR_PORT}/tcp': CONNECTOR_PORT})

    def start_midpoint(self, local=False):
        self.start_container(
            MIDPOINT_DOCKER, local, entrypoint='./bin/spawn.sh', ports={f'{MIDPOINT_PORT}/tcp': MIDPOINT_PORT})

    def start_api_gateway(self, local=False):
        self.start_container(
            API_GW_DOCKER, local, entrypoint='./bin/spawn.sh', ports={f'{API_GW_PORT}/tcp': API_GW_PORT})

    def start_container(self, image, local, **kwargs):
        client = docker.from_env()
        if 'name' not in kwargs:
            kwargs.update({'name': image})
        container = client.containers.run(
            image=image,
            detach=True, auto_remove=True, network="host" if local else "sparkle-net", **kwargs
        )
        self.modules.append(container)

    def start_database(self):
        volume = '{}/schema.sql'.format(os.getenv("MISC"))
        self.start_container('postgres:12', name='sparkledb', ports={'5432/tcp': 5432}, environment=['POSTGRES_PASSWORD=foo'],
                             volumes={volume: {'bind': '/docker-entrypoint-initdb.d/schema.sql', 'mode': 'rw'}})

    def wait_for_database(self, timeout=15.0):
        start_time = timer()
        while True:
            try:
                self.db_conn = psycopg2.connect(
                    database='sparkledb', user='sparkle', host='127.0.0.1', password='foobar')
                return
            except:
                pass

            if (timer() - start_time > timeout):
                self.fail('Waited to long for database connection.')
            time.sleep(5)

    def wait_for_connector(self):
        self.wait_for(CONNECTOR_PORT, CONNECTOR_HOST)

    def wait_for_midpoint(self):
        self.wait_for(MIDPOINT_PORT, MIDPOINT_HOST)

    def wait_for_api_gateway(self):
        self.wait_for(API_GW_PORT, API_GW_HOST)

    def wait_for(self, port, host, timeout=15.0):
        start_time = time.perf_counter()
        while True:
            try:
                with socket.create_connection((host, port), timeout=timeout):
                    break
            except OSError as ex:
                time.sleep(0.1)
                if time.perf_counter() - start_time >= timeout:
                    self.fail(
                        'Waited too long for the port {} on host {} to start accepting connections.'.format(port, host))
        time.sleep(5)

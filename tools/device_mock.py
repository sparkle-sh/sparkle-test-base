#!./venv/bin/python3.7

from argparse import ArgumentParser
from fakes.fake_driver import FakeDriver
from models.device import *


def start_switchable_device(client, device):
    state = 0
    while True:
        header, content = client.get_validated_request()

        if header == 'switch_device_state_request':
            res = {
                "header": "ack_response",
                "content": {}
            }
            new_state = content.get("state")
            print(f"I have changed state from {state} to {new_state}")
            state = new_state
            client.send_response(res)

        if header == 'get_device_state_request':
            res = {
                "header": "get_device_state_response",
                "content": {
                    "state": state
                }
            }
            client.send_response(res)

        if header == 'get_device_datasheet_request':
            res = {
                "header": "get_device_datasheet_response",
                "content": {
                    "datasheet": {
                        "states": [0, 1]
                    }
                }
            }
            client.send_response(res)


def start_sensor(client, device):
    while True:
        header, content = client.get_validated_request()

        if header == 'get_sensor_value_request':
            res = {
                "header": "get_sensor_value_response",
                "content": {
                    "values": {
                        "value": 1
                    }
                }
            }
            client.send_response(res)

        if header == 'get_device_datasheet_request':
            res = {
                "header": "get_device_datasheet_response",
                "content": {
                    "datasheet": {
                        "labels": ["value"]
                    }
                }
            }
            client.send_response(res)


def start(args):
    client = FakeDriver()
    client.connect(args.host, int(args.port))
    client.sock.settimeout(None)
    client.send_handshake()

    device = None
    if args.type == 'sensor':
        device = Device(DeviceType.SENSOR, args.name, args.description,
                        SensorDeviceDatasheet(["value"]))
    elif args.type == 'switchable':
        device = Device(DeviceType.SWITCHABLE, args.name, args.description)
    else:
        raise RuntimeError("Invalid device type")
    client.register_devices([device])

    if args.type == 'sensor':
        start_sensor(client, device)
    else:
        start_switchable_device(client, device)


def main():
    parser = ArgumentParser()
    parser.add_argument("--host", help="Connector host", required=True)
    parser.add_argument("-p", "--port", help="Connector port", required=True)
    parser.add_argument("-n", "--name", help="Device name", required=True)
    parser.add_argument("-d", "--description",
                        help="Device description", required=True)
    parser.add_argument(
        "-t", "--type", help="Device type (sensor/switchable)", required=True)

    args = parser.parse_args()
    start(args)


if __name__ == '__main__':
    main()

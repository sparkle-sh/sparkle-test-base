#!./venv/bin/python3.7

from argparse import ArgumentParser
from fakes.fake_driver import FakeDriver
from models.device import *


def listen_for_events(client, device):
    while True:
        header, content = client.get_validated_response()


def start(args):
    client = FakeDriver()
    client.connect(args.host, int(args.port))
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
    listen_for_events(client, device)


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

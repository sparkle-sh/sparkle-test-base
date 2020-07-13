from .connector_client import ConnectorClient


class FakeDriver(ConnectorClient):
    def __init__(self):
        print("starting")
        super().__init__(session_type='driver')

    def disconnect(self):
        super().disconnect()

    def register_devices(self, devices):
        payload = {
            "header": "register_devices_request",
            "content": {
                "devices": [device.serialize() for device in devices]
            }
        }

        self.send_request(payload)
        res = self.get_response()

        assert res.get('header') == 'ack_response'

    def send_device_info(self, version):
        payload = {
            "header": "get_device_info_response",
            "content": {
                "version": version
            }
        }
        return self._request(payload, False, False)

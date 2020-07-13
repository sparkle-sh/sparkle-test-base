from .connector_client import ConnectorClient

class DriverClient(ConnectorClient):
    def __init__(self):
        print("starting")
        super().__init__(session_type='driver')

    def disconnect(self):
        # request = {
        #     "header": "disconnect_request",
        #     "content": {}
        # }

        # self.send_request(request)
        # response = self.get_response()
        # assert response.get('header') == 'ack_response'

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

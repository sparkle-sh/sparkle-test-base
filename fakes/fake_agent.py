from .connector_client import ConnectorClient


class FakeAgent(ConnectorClient):
    def __init__(self):
        print("starting")
        super().__init__(session_type='agent')

    def disconnect(self):
        request = {
            "header": "disconnect_request",
            "content": {}
        }

        self.send_request(request)
        response = self.get_response()
        assert response.get('header') == 'ack_response'

        super().disconnect()

    def list_devices(self, wait=True, check=True):
        payload = {
            "header": "list_devices_request",
            "content": {
            }
        }
        return self._request(payload, wait, check)

    def get_device_info(self, device_id, wait=True, check=True):
         payload = {
            "header": "get_device_info_request",
            "content": {
                "device_id": device_id
            }
        }
        return self._request(payload, wait, check)


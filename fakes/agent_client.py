from .connector_client import ConnectorClient

class AgentClient(ConnectorClient):
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

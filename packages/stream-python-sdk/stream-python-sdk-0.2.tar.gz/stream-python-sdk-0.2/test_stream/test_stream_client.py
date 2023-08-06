# -*- coding:utf8 -*-

import json

from stream.client import stream_client

class TestClient():

    def __init__(self):
        self.access_key_id = 'access_key_id'
        self.access_key_secret = 'access_key_secret'
        self.topic_name = 'topic_name'
        self.position_type = 'EARLIEST'
        self.logs_position = ""
        self.limit = 1
        self.client = stream_client.StreamClient(
            self.access_key_id, self.access_key_secret)

    def test_get_subscription_position(self):
        """ Get subscription position."""
        response = self.client.get_subscription_position(
            subscription_name=self.topic_name,
            position_type=self.position_type
        )
        return response

    def test_get_logs(self):
        """ Get_logs."""
        response = self.test_get_subscription_position()
        response = json.loads(response)
        self.logs_position = response['result']['position']
        response = self.client.get_logs(
            subscription_name=self.topic_name,
            logs_position=self.logs_position,
            limit=self.limit
        )
        return response

print TestClient().test_get_subscription_position()
print TestClient().test_get_logs()
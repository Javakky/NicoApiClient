import datetime

import requests

from nicovideo_api_client.constants import JSON


class MockResponse(requests.Response):
    def __init__(self, json_data: JSON, status_code: int, time: datetime.timedelta):
        super().__init__()
        self.json_data = json_data
        self.status_code = status_code
        self.elapsed = time

    def json(self):
        return self.json_data

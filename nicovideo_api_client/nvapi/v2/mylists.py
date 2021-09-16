from typing import Dict

from nicovideo_api_client.nvapi.v2.request import SnapshotSearchNVAPIV2Request


class SnapshotSearchNVAPIV2Mylists:
    def __init__(self, endpoint: str, mylist_id: str):
        self.endpoint = endpoint + mylist_id
        self.query: Dict[str, str] = {}

    def limit(self, limit: int) -> SnapshotSearchNVAPIV2Request:
        return SnapshotSearchNVAPIV2Request(self.endpoint, self.query, limit)

from typing import Dict

from nicovideo_api_client.nvapi.v3.request import SnapshotSearchNVAPIV3Request


class SnapshotSearchNVAPIV3Limit:
    def __init__(self, endpoint: str, query: Dict[str, str]):
        self.endpoint = endpoint
        self.query: Dict[str, str] = query

    def limit(self, limit: int) -> SnapshotSearchNVAPIV3Request:
        return SnapshotSearchNVAPIV3Request(self.endpoint, self.query, limit)

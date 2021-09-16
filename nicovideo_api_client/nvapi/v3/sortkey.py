from typing import Dict

from nicovideo_api_client.nvapi.v3.limit import SnapshotSearchNVAPIV3Limit


class SnapshotSearchNVAPIV3SortKey:
    def __init__(self, endpoint: str, query: Dict[str, str]):
        self.endpoint = endpoint
        self.query: Dict[str, str] = query

    def sort_order(self, asc: bool) -> SnapshotSearchNVAPIV3Limit:
        self.query['sortOrder'] = 'asc' if asc else 'desc'
        return SnapshotSearchNVAPIV3Limit(self.endpoint, self.query)

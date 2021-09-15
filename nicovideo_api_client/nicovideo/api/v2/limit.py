from typing import Dict

from nicovideo_api_client.nicovideo.api.v2.request import SnapshotSearchAPIV2Request


class SnapshotSearchAPIV2Limit:

    def __init__(self, query: Dict[str, str]):
        self.query: Dict[str, str] = query

    def limit(self, limit: int = 4) -> SnapshotSearchAPIV2Request:
        return SnapshotSearchAPIV2Request(self.query, limit)

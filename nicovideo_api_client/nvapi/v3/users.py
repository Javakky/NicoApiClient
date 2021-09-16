from typing import Dict

from nicovideo_api_client.constants import SortKeyType
from nicovideo_api_client.nvapi.v3.sortkey import SnapshotSearchNVAPIV3SortKey


class SnapshotSearchNVAPIV3Users:
    def __init__(self, endpoint: str, user_id: int):
        self.endpoint = endpoint + f'users/{user_id}/videos'
        self.query: Dict[str, str] = {}

    def sort_key(self, sort_key_type: SortKeyType) -> SnapshotSearchNVAPIV3SortKey:
        self.query['sortKey'] = sort_key_type.value
        return SnapshotSearchNVAPIV3SortKey(self.endpoint, self.query)

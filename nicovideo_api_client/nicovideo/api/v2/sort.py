from typing import Dict

from nicovideo_api_client.nicovideo.constants import FieldType, sort_types
from nicovideo_api_client.nicovideo.api.v2.filter import SnapshotSearchAPIV2Filter


class SnapshotSearchAPIV2Sort:
    def __init__(self, query: Dict[str, str]):
        self.query: Dict[str, str] = query

    def sort(self, sort_type: FieldType, reverse: bool = False) -> SnapshotSearchAPIV2Filter:
        if sort_type not in sort_types:
            raise Exception("不正なソートタイプ")
        self.query['_sort'] = ('+' if reverse else '-') + sort_type.value
        return SnapshotSearchAPIV2Filter(self.query)

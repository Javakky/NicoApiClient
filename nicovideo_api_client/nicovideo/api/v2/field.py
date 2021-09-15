from typing import Dict, Set

from nicovideo_api_client.nicovideo.constants import FieldType
from nicovideo_api_client.nicovideo.api.v2.sort import SnapshotSearchAPIV2Sort


class SnapshotSearchAPIV2Fields:
    def __init__(self, query: Dict[str, str]):
        self.fields: Set[str] = set()
        self.query: Dict[str, str] = query

    def field(self, fields: Set[FieldType]) -> 'SnapshotSearchAPIV2Sort':
        self.fields = set(map(lambda x: x.value, fields))
        if len(self.fields) > 0:
            self.query["fields"] = ','.join(self.fields)
        return SnapshotSearchAPIV2Sort(self.query)

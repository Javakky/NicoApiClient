from typing import Dict

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields


class SnapshotSearchAPIV2TagsExact:
    def __init__(self):
        self._query: Dict[str, str] = {'targets': 'tagsExact'}

    def query(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        self._query['q'] = keyword
        return SnapshotSearchAPIV2Fields(self._query)


class SnapshotSearchAPIV2Keywords:
    def __init__(self):
        self._query: Dict[str, str] = {'targets': 'title,description,tags'}

    def query(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        self._query['q'] = keyword
        return SnapshotSearchAPIV2Fields(self._query)

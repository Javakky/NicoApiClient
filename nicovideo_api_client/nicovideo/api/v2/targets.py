from typing import Dict

from nicovideo_api_client.nicovideo.api.v2.field import SnapshotSearchAPIV2Fields


class SnapshotSearchAPIV2TagsExact:
    def __init__(self):
        self.query: Dict[str, str] = {'targets': 'tagsExact'}

    def q(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        self.query['q'] = keyword
        return SnapshotSearchAPIV2Fields(self.query)


class SnapshotSearchAPIV2Keywords:
    def __init__(self):
        self.query: Dict[str, str] = {'targets': 'title,description,tags'}

    def q(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        self.query['q'] = keyword
        return SnapshotSearchAPIV2Fields(self.query)

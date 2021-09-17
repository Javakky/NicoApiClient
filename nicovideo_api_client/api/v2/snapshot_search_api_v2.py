from datetime import datetime

import requests

from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2TagsExact, SnapshotSearchAPIV2Keywords
from nicovideo_api_client.constants import END_POINT_URL_V2_VERSION


class SnapshotSearchAPIV2:
    @staticmethod
    def tags_exact() -> 'SnapshotSearchAPIV2TagsExact':
        return SnapshotSearchAPIV2TagsExact()

    @staticmethod
    def keywords() -> 'SnapshotSearchAPIV2Keywords':
        return SnapshotSearchAPIV2Keywords()

    @staticmethod
    def version(timeout: float = 400) -> datetime:
        json = requests.get(END_POINT_URL_V2_VERSION, timeout=timeout).json()
        return datetime.fromisoformat(json["last_modified"])

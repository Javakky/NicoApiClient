from datetime import datetime

import requests

from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2TagsExact, SnapshotSearchAPIV2Keywords


class SnapshotSearchAPIV2:
    @staticmethod
    def tags_exact() -> 'SnapshotSearchAPIV2TagsExact':
        return SnapshotSearchAPIV2TagsExact()

    @staticmethod
    def keywords() -> 'SnapshotSearchAPIV2Keywords':
        return SnapshotSearchAPIV2Keywords()

    @staticmethod
    def version(timeout: float = 400) -> datetime:
        json = requests.get("https://api.search.nicovideo.jp/api/v2/snapshot/version", timeout=timeout).json()
        return datetime.fromisoformat(json["last_modified"])

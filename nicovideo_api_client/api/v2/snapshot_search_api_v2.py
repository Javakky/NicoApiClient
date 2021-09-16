from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2TagsExact, SnapshotSearchAPIV2Keywords


class SnapshotSearchAPIV2:
    @staticmethod
    def tags_exact() -> 'SnapshotSearchAPIV2TagsExact':
        return SnapshotSearchAPIV2TagsExact()

    @staticmethod
    def keywords() -> 'SnapshotSearchAPIV2Keywords':
        return SnapshotSearchAPIV2Keywords()

from nicovideo_api_client.nicovideo.api.v2.targets import SnapshotSearchAPIV2TagsExact, SnapshotSearchAPIV2Keywords


class SnapshotSearchAPIV2:
    def tagsExact(self) -> 'SnapshotSearchAPIV2TagsExact':
        return SnapshotSearchAPIV2TagsExact()

    def keywords(self) -> 'SnapshotSearchAPIV2Keywords':
        return SnapshotSearchAPIV2Keywords()

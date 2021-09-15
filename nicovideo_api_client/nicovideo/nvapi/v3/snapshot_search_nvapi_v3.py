from nicovideo_api_client.nicovideo.constants import END_POINT_URL_NVV3
from nicovideo_api_client.nicovideo.nvapi.v3.users import SnapshotSearchNVAPIV3Users


class SnapshotSearchNVAPIV3:

    def users(self, user_id: int) -> SnapshotSearchNVAPIV3Users:
        return SnapshotSearchNVAPIV3Users(END_POINT_URL_NVV3, user_id)

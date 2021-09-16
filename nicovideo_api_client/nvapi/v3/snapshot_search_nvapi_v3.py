from nicovideo_api_client.constants import END_POINT_URL_NVV3
from nicovideo_api_client.nvapi.v3.users import SnapshotSearchNVAPIV3Users


class SnapshotSearchNVAPIV3:

    @staticmethod
    def users(user_id: int) -> SnapshotSearchNVAPIV3Users:
        return SnapshotSearchNVAPIV3Users(END_POINT_URL_NVV3, user_id)

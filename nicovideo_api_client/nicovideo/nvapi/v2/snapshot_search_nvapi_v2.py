from typing import Union

from nicovideo_api_client.nicovideo.constants import END_POINT_URL_NVV3, END_POINT_URL_NVV2
from nicovideo_api_client.nicovideo.nvapi.v2.mylists import SnapshotSearchNVAPIV2Mylists
from nicovideo_api_client.nicovideo.nvapi.v3.users import SnapshotSearchNVAPIV3Users


class SnapshotSearchNVAPIV2:

    def mylists(self, mylist_id: Union[int, str]) -> SnapshotSearchNVAPIV2Mylists:
        if isinstance(mylist_id, int):
            mylist_id_str = f'mylists/{mylist_id}'
        else:
            mylist_id_str = mylist_id
        return SnapshotSearchNVAPIV2Mylists(END_POINT_URL_NVV2, mylist_id_str)

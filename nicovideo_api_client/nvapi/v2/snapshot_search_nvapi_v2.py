from typing import Union

from nicovideo_api_client.constants import END_POINT_URL_NVV2
from nicovideo_api_client.nvapi.v2.mylists import SnapshotSearchNVAPIV2Mylists


class SnapshotSearchNVAPIV2:

    @staticmethod
    def mylists(mylist_id: Union[int, str]) -> SnapshotSearchNVAPIV2Mylists:
        if isinstance(mylist_id, int):
            mylist_id_str = f'mylists/{mylist_id}'
        else:
            mylist_id_str = mylist_id
        return SnapshotSearchNVAPIV2Mylists(END_POINT_URL_NVV2, mylist_id_str)
